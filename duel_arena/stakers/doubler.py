from duel_arena.stakers.abstract import AbstractStaker
from duel_arena.stakers.exceptions import NotEnoughGpException


class DoublerStaker(AbstractStaker):
    default_wage_decimal = None
    current_loss = 0

    def __init__(self, gp, default_wage_decimal=.0001):
        """Initializes gp and default_wager."""
        self.default_wage_decimal = default_wage_decimal
        super(DoublerStaker, self).__init__(gp)
        self.current_loss = 0

    def propose_stake(self):
        """Proposes gp for a stake."""
        if self.is_first_duel or self.won_last_duel:
            wager = self.default_wager()
        else:
            wager = self.double_wager()
        return self._propose_stake(wager)

    def accept_stake(self, gp):
        """Returns True if the staker will accept."""
        if self.is_first_duel or self.won_last_duel:
            accepted = self.default_wager() == gp
        else:
            accepted = self.double_wager() == gp
        return self._accept_stake(gp, accepted)

    def lose_duel(self, staked_gp):
        self.current_loss = staked_gp
        return super(DoublerStaker, self).lose_duel(staked_gp)

    def default_wager(self):
        """Default wager for this staker"""
        return self.starting_gp * self.default_wage_decimal

    def double_wager(self):
        """Doubles the total loss in the the simulation."""
        return self.current_loss * 2

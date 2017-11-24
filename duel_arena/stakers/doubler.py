from duel_arena.stakers.abstract import AbstractStaker
from duel_arena.stakers.exceptions import NotEnoughGpException


class DoublerStaker(AbstractStaker):
    default_wage_decimal = None
    current_loss = 0

    def __init__(self, gp, default_wage_decimal=.001):
        """Initializes gp and default_wager."""
        self.default_wage_decimal = default_wage_decimal
        super(DoublerStaker, self).__init__(gp)
        self.current_loss = self.default_wager()

    def accept_stake(self, gp):
        """Returns True if the staker will accept."""
        if self.is_first_duel or self.won_last_duel:
            return self.default_wager() == gp
        else:
            return self.double_wager() == gp

    def propose_stake(self):
        """Proposes gp for a stake."""
        if self.is_first_duel or self.won_last_duel:
            return self.default_wager()
        else:
            return self.double_wager()

    def lose_duel(self, staked_gp):
        self.current_loss = staked_gp
        return super(DoublerStaker, self).lose_duel(staked_gp)

    def default_wager(self):
        """Default wager for this staker"""
        wager = int(self.starting_gp / 100)
        if wager > self.current_gp:
            raise NotEnoughGpException("Double staker doesnt have enough gp for default wager")
        return wager

    def double_wager(self):
        """Doubles the total loss in the the simulation."""
        double_current_loss = self.current_loss * 2
        if double_current_loss > self.current_gp:
            raise NotEnoughGpException("Double staker can no longer double.")
        return double_current_loss

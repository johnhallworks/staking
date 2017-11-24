from random import randint

from duel_arena.stakers.abstract import AbstractStaker
from duel_arena.stakers.exceptions import NotEnoughGpException


class IndifferentStaker(AbstractStaker):
    _indifference = None

    def __init__(self, gp, indifference=1):
        self._indifference = indifference
        super(IndifferentStaker, self).__init__(gp)

    def propose_stake(self):
        """Willing to propose any stake within the indifference threshold."""
        return self._propose_stake(randint(0, self.indifference_threshold()))

    def accept_stake(self, gp):
        """Accepts if the proposed gp is below an indifference threshold."""
        return self._accept_stake(gp, gp < self.indifference_threshold())

    def indifference_threshold(self):
        threshold = int(self.current_gp * self._indifference)
        if threshold < 1:
            threshold = self.current_gp
        return threshold

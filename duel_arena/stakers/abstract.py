from abc import ABCMeta, abstractmethod
from uuid import uuid4

from duel_arena.stakers.exceptions import NotEnoughGpException


class AbstractStaker(object):
    __metaclass__ = ABCMeta
    id = None
    starting_gp = None
    _current_gp = None
    duel_history = None

    def __init__(self, starting_gp):
        if type(starting_gp) != int:
            raise TypeError("gp must be an int not: {0}".format(type(starting_gp)))
        self.id = str(uuid4())
        self.duel_history = []
        self.starting_gp = starting_gp
        self.current_gp = starting_gp

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.id)

    @property
    def current_gp(self):
        return self._current_gp

    @current_gp.setter
    def current_gp(self, gp):
        if gp < 0:
            raise ValueError("Oops, {0} attempted to stake more money than they have."
                             .format(self.__str__()))
        self._current_gp = gp

    @property
    def is_first_duel(self):
        return len(self.duel_history) == 0

    @property
    def won_last_duel(self):
        return len(self.duel_history) > 0 and self.duel_history[-1]

    @property
    def wins(self):
        return len([duel for duel in self.duel_history if duel])

    @property
    def losses(self):
        return len([duel for duel in self.duel_history if not duel])

    @abstractmethod
    def propose_stake(self):
        raise NotImplementedError("Method must be implemented in inheriting class")

    def _propose_stake(self, gp):
        if self.current_gp <=0:
            raise NotEnoughGpException("{0} has no Gp".format(self.__str__()))
        return min(gp, self.current_gp)

    def _accept_stake(self, gp, accepted):
        if self.current_gp <=0:
            raise NotEnoughGpException("{0} has no Gp".format(self.__str__()))
        return accepted and gp <= self.current_gp

    @abstractmethod
    def accept_stake(self, gp):
        raise NotImplementedError("Method must be implemented in inheriting class")

    def win_duel(self, staked_gp):
        self.current_gp = self.current_gp + staked_gp
        self.duel_history.append(True)

    def lose_duel(self, staked_gp):
        self.current_gp = self.current_gp - staked_gp
        self.duel_history.append(False)

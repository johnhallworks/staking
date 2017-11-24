from duel_arena.stakers.exceptions import NotEnoughGpException

from duel_arena.stakers.abstract import AbstractStaker


class FibonacciStaker(AbstractStaker):

    def __init__(self, starting_gp, multiplier=.005):
        self._fib_num = 1
        self._multiplier = multiplier
        super(FibonacciStaker, self).__init__(starting_gp)

    @staticmethod
    def fibonacci(i):
        if i == 0 or i == 1:
            return 1
        return (FibonacciStaker.fibonacci(i - 1) +
                FibonacciStaker.fibonacci(i - 2))

    def fib_stake(self):
        return (self.current_gp *
                self._multiplier *
                self.fibonacci(self._fib_num))

    def propose_stake(self):
        fib_stake = self.fib_stake()
        if fib_stake > self.current_gp:
            raise NotEnoughGpException("Fib staker cant fib stake")
        return fib_stake

    def accept_stake(self, gp):
        fib_stake = self.fib_stake()
        if gp == fib_stake:
            if fib_stake > self.current_gp:
                raise NotEnoughGpException("Fib staker cant fib stake")
            return True
        return False

    def win_duel(self, staked_gp):
        if self._fib_num > 1:
            self._fib_num -= 1
        super(FibonacciStaker, self).win_duel(staked_gp)

    def lose_duel(self, staked_gp):
        self._fib_num += 1
        super(FibonacciStaker, self).lose_duel(staked_gp)

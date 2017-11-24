from duel_arena.stakers.abstract import AbstractStaker


class FibonacciStaker(AbstractStaker):

    def __init__(self, starting_gp, multiplier=.00001):
        self._fib_num = 1
        self._multiplier = multiplier
        super(FibonacciStaker, self).__init__(starting_gp)

    @staticmethod
    def fibonacci(i, memo = None):
        if memo is None:
            memo = {0: 1, 1: 1}
        if i <= 1:
            return 1
        number = (FibonacciStaker.fibonacci(i - 1, memo) +
                  FibonacciStaker.fibonacci(i - 2, memo))
        if i not in memo:
            memo[i] = number
        return number

    def fib_stake(self):
        return int(self.current_gp *
                   self._multiplier *
                   self.fibonacci(self._fib_num))

    def propose_stake(self):
        return self._propose_stake(self.fib_stake())

    def accept_stake(self, gp):
        fib_stake = self.fib_stake()
        return self._accept_stake(gp, fib_stake == gp)

    def win_duel(self, staked_gp):
        if self._fib_num > 1:
            self._fib_num -= 1
        super(FibonacciStaker, self).win_duel(staked_gp)

    def lose_duel(self, staked_gp):
        self._fib_num += 1
        super(FibonacciStaker, self).lose_duel(staked_gp)

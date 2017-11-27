import signal
from random import randint

from stakers.exceptions import NotEnoughGpException


class DuelArenaSimulator(object):
    stakers = None
    max_stakes = None

    interrupted = False
    default_int_handler = None

    def __init__(self, stakers, max_stakes=100000):
        """Initializes the simulation."""
        self.stakers = stakers
        self.max_stakes = max_stakes

        self.interrupted = False
        self.default_int_handler = signal.signal(signal.SIGINT, self.end_simulation)

    def end_simulation(self, signum, frame):
        print("Simulation ended by sigint")
        self.interrupted = True
        signal.signal(signal.SIGINT, self.default_int_handler)

    def simulate(self):
        """Simulates duel arena staking."""
        self.interrupted = False
        stakes = 0

        while stakes < self.max_stakes and not self.interrupted and self.stakers_can_stake():
            for proposing_staker in self.stakers:
                accepting_staker = self.choose_opponent(proposing_staker, self.stakers)
                if proposing_staker.current_gp != 0 and accepting_staker.current_gp != 0:
                    self.attempt_stake(proposing_staker, accepting_staker)
            stakes += 1

    @staticmethod
    def choose_opponent(proposing_staker, stakers):
        """Chooses a random opponent."""
        accepting_staker = stakers[randint(0, len(stakers) - 1)]
        while proposing_staker == accepting_staker:
            accepting_staker = stakers[randint(0, len(stakers) - 1)]
        return accepting_staker

    @staticmethod
    def attempt_stake(proposing_staker, accepting_staker):
        """Propose a stake, if accepted, stake then handle results."""
        try:
            proposed_gp = proposing_staker.propose_stake()
            if accepting_staker.accept_stake(proposed_gp):
                proposed_staker_wins = randint(0, 1)
                if proposed_staker_wins:
                    DuelArenaSimulator.handle_duel_results(
                        proposing_staker, accepting_staker, proposed_gp)
                else:
                    DuelArenaSimulator.handle_duel_results(
                        accepting_staker, proposing_staker, proposed_gp)
                return True
        except NotEnoughGpException as ex:
            pass
        return False

    @staticmethod
    def handle_duel_results(winner, loser, gp):
        """Distributes winnings and losses."""
        winner.win_duel(gp)
        loser.lose_duel(gp)

    def reset_variables(self, stakers=None, max_stakes=None):
        self.__init__(stakers, max_stakes)

    def stakers_can_stake(self):
        return len([staker for staker in self.stakers if staker.current_gp > 0]) > 0

    def results(self):
        """Gives some basic results by staker type."""
        results = {}
        for staker in self.stakers:
            staker_type = staker.__class__.__name__
            if staker_type not in results:
                results[staker_type] = {
                    "wins": 0,
                    "losses": 0,
                    "current_gp": 0,
                    "starting_gp": 0
                }
            results[staker_type]["wins"] += staker.wins
            results[staker_type]["losses"] += staker.losses
            results[staker_type]["starting_gp"] += staker.starting_gp
            results[staker_type]["current_gp"] += staker.current_gp
        return results

from random import randint

from stakers.exceptions import NotEnoughGpException


class DuelArenaSimulator(object):
    stakers = None
    stakes = 0
    max_stakes = None

    def __init__(self, stakers, max_stakes=None):
        self.stakers = stakers
        self.stakes = 0
        self.max_stakes = max_stakes

    def simulate(self):
        """Simulates duel arena staking."""
        someone_staked = True
        while someone_staked and (self.max_stakes is None
                                  or self.stakes < self.max_stakes):
            someone_staked = False
            for proposing_staker in self.stakers:
                accepting_staker = self.choose_opponent(proposing_staker, self.stakers)
                stake_happened = self.attempt_stake(proposing_staker, accepting_staker)
                if stake_happened:
                    someone_staked = True
            if someone_staked:
                self.stakes += 1
        if not someone_staked:
            print("No one was left to stake")

    @staticmethod
    def choose_opponent(proposing_staker, stakers):
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
        winner.win_duel(gp)
        loser.lose_duel(gp)

    def results(self):
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

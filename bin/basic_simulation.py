from random import shuffle

from duel_arena.simulator import DuelArenaSimulator
from duel_arena.stakers.doubler import DoublerStaker
from duel_arena.stakers.fibonacci import FibonacciStaker
from duel_arena.stakers.indifferent import IndifferentStaker


def print_basic_results(completed_sim):
    for staker_type, results in completed_sim.results().items():
        print("{0}:\n\twins: {1}\n\tlosses {2}\n\tstarting GP: {3}\n\tending GP {4}\n\t"
              "better off: {5}\n\tdiference: {6}%"
              .format(staker_type, results["wins"], results["losses"],
                      results["starting_gp"], results["current_gp"],
                      results["current_gp"] > results["starting_gp"],
                      (float(results["current_gp"] - results["starting_gp"]) / results["starting_gp"])*100))


if __name__ == "__main__":
    stakers = []
    starting_gp = 1000000
    for i in range(1):
        stakers.append(FibonacciStaker(starting_gp))
        stakers.append(IndifferentStaker(starting_gp))
        stakers.append(DoublerStaker(starting_gp))
    shuffle(stakers)

    simulator = DuelArenaSimulator(stakers)
    simulator.simulate()
    print_basic_results(simulator)

import multiprocessing
from itertools import combinations


num_processes = multiprocessing.cpu_count()

def get_all_equity(current_cards : list[object],remaining_cards : list[object]) -> list[float]:
    all_combinations = list(combinations(remaining_cards, 7-len(current_cards[0])))
    print(all_combinations[0])
    return 0

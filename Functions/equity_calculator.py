
import multiprocessing
from itertools import combinations
from Functions import hand_evaluator

num_processes = multiprocessing.cpu_count()

def process_hand_winner(player_total_wins : list[int],current_cards : list[object], card_combinations : tuple[object]):
    for combination in card_combinations:
        hand_with_combination = current_cards.copy()
        winner = hand_evaluator.evaluate_hand(hand_with_combination.extend(combination))
        with lock:
            player_total_wins[winner] += 1

def get_all_equity(current_cards : list[object],remaining_cards : list[object]) -> list[float]:
    all_combinations = list(combinations(remaining_cards, 7-len(current_cards[0])))
    num_processes = multiprocessing.cpu_count()
    player_total_wins = multiprocessing.Array('i',[0 for player in range(0,len(current_cards))])
    lock = multiprocessing.Lock()

    return 0


import time
import multiprocessing
import random

def worker(shared_array, lock):
    for _ in range(100):  # each worker will perform 100 increments
        index = random.randint(0, len(shared_array) - 1)
        with lock:
            shared_array[index] += 1

if __name__ == "__main__":
    t = time.time()
    
    # Create a shared array initialized to [0, 0, 0, 0, 0, 0, 0]
    shared_array = multiprocessing.Array('i', [0, 0, 0, 0, 0, 0, 0])
    
    # Create a lock to synchronize access to the shared array
    lock = multiprocessing.Lock()
    
    # Create and start 3 processes
    processes = [multiprocessing.Process(target=worker, args=(shared_array, lock)) for _ in range(3)]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()

    # Print the final values of the shared array
    print("time=", time.time() - t)
    print("Final shared array:", list(shared_array))

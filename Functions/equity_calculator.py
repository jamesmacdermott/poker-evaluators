import multiprocessing
from itertools import combinations
from . import hand_evaluator
import copy



def queue_evaluated_segment(result_queue,playerscards_array,segment_of_combinations):
    for hand in segment_of_combinations:
        cards_for_combo = copy.deepcopy(playerscards_array)
        for player in cards_for_combo:
            player.extend(hand)

        winner = hand_evaluator.evaluate_hand(cards_for_combo)
        if type(winner) == int:
            result_queue.put(winner)
 

def find_equity(playerscards_array,rem_cards):
    num_processes = multiprocessing.cpu_count()  # Number of processes
    result_queue = multiprocessing.Queue()  # Queue to store results

    processes = []
    needed = 7-len(playerscards_array[0])
    combos_of_remaining = list(combinations(rem_cards, needed))
    # for all combos use : combos_of_remaining[int(segment * (len(combos_of_remaining) / num_segments)):int((segment + 1) * (len(combos_of_remaining) / num_segments))]

    num_segments = multiprocessing.cpu_count()
    for segment in range(num_processes):
        p = multiprocessing.Process(target=queue_evaluated_segment, args=(result_queue,playerscards_array,combos_of_remaining[int(segment * (len(combos_of_remaining) / num_segments)):int((segment + 1) * (len(combos_of_remaining) / num_segments))]))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()


    # Retrieve results from the queue and sum all arrays
    results = [0 for player in range(len(playerscards_array))]
    while not result_queue.empty():
        results[result_queue.get()] += 1

    print("Final array:", results)
    return results

if __name__ == '__main__':
    pass
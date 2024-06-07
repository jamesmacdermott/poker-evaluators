import multiprocessing
import random

def add_random_numbers(result_queue):
    random_numbers = [random.randint(1, 100) for _ in range(3)]
    result_queue.put(random_numbers)

def __func__():
    num_processes = 4  # Number of processes
    result_queue = multiprocessing.Queue()  # Queue to store results

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=add_random_numbers, args=(result_queue,))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Retrieve results from the queue and sum all arrays
    final_array = []
    while not result_queue.empty():
        final_array += result_queue.get()

    print("Final array:", final_array)
    print("Sum of all arrays:", sum(final_array))

if __name__ == "__main__":
    __func__()

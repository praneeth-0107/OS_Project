import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import math
import random

# ---------------------------------------------------
# DATA PARALLELISM
# ---------------------------------------------------
def heavy_data_task(nums):
    """Sum of cubes - CPU heavy task"""
    total = 0
    for x in nums:
        total += x ** 3
    return total

def data_parallel_demo(n=50_000_000):
    print("\n=== DATA PARALLELISM DEMONSTRATION ===")
    data = list(range(n))
    n_cores = mp.cpu_count()
    print(f"CPU cores available: {n_cores}")

    chunk_size = len(data) // n_cores
    chunks = [data[i*chunk_size:(i+1)*chunk_size] for i in range(n_cores)]

    # Serial Execution
    t0 = time.perf_counter()
    serial_result = sum(x**3 for x in data)
    serial_time = time.perf_counter() - t0
    print(f"Serial result: {serial_result}")
    print(f"Serial time: {serial_time:.4f}s")

    # Parallel Execution
    t1 = time.perf_counter()
    with mp.Pool(processes=n_cores) as pool:
        results = pool.map(heavy_data_task, chunks)
    parallel_result = sum(results)
    parallel_time = time.perf_counter() - t1
    print(f"Parallel result: {parallel_result}")
    print(f"Parallel time: {parallel_time:.4f}s")

    # Speedup
    speedup = serial_time / parallel_time
    efficiency = (speedup / n_cores) * 100
    print(f"Speedup: {speedup:.2f}x")
    print(f"Efficiency: {efficiency:.2f}%\n")


# ---------------------------------------------------
# TASK PARALLELISM
# ---------------------------------------------------
def factorial_task(n):
    res = 1
    for i in range(2, n+1):
        res *= i
    return f"Factorial({n}) done"

def sum_primes_task(limit):
    sieve = [True]*(limit+1)
    sieve[0:2] = [False, False]
    for i in range(2, int(math.sqrt(limit))+1):
        if sieve[i]:
            for j in range(i*i, limit+1, i):
                sieve[j] = False
    total = sum(i for i, val in enumerate(sieve) if val)
    return f"Sum of primes ≤ {limit}: {total}"

def sort_task(size):
    arr = [random.randint(0, 10**6) for _ in range(size)]
    arr.sort()
    return f"Sorted list of {size} elements"

def task_parallel_demo():
    print("\n=== TASK PARALLELISM DEMONSTRATION ===")
    n_cores = mp.cpu_count()
    print(f"CPU cores available: {n_cores}")

    tasks = [
        (factorial_task, 50000),      # bigger factorial
        (sum_primes_task, 2000000),   # bigger prime sum
        (sort_task, 10000000)         # bigger list
    ]

    # Serial Execution
    t0 = time.perf_counter()
    serial_results = [func(arg) for func, arg in tasks]
    serial_time = time.perf_counter() - t0
    print("\n-- Serial Results --")
    for r in serial_results:
        print(r)
    print(f"Serial time: {serial_time:.4f}s")

    # Parallel Execution
    t1 = time.perf_counter()
    parallel_results = []
    with ProcessPoolExecutor(max_workers=min(len(tasks), n_cores)) as executor:
        futures = [executor.submit(func, arg) for func, arg in tasks]
        for f in futures:
            parallel_results.append(f.result())
    parallel_time = time.perf_counter() - t1

    print("\n-- Parallel Results --")
    for r in parallel_results:
        print(r)
    print(f"Parallel time: {parallel_time:.4f}s")

    # Speedup
    speedup = serial_time / parallel_time
    efficiency = (speedup / n_cores) * 100
    print("\n=== PERFORMANCE SUMMARY ===")
    print(f"Serial Time   : {serial_time:.4f}s")
    print(f"Parallel Time : {parallel_time:.4f}s")
    print(f"Speedup       : {speedup:.2f}x")
    print(f"Efficiency    : {efficiency:.2f}%\n")


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":
    data_parallel_demo()
    task_parallel_demo()

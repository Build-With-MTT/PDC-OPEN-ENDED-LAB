# partB_d.py - Part B(d): better work division  (RUN THIS ON UBUNTU)
# Equal chunks are unfair: big numbers need more trial divisions, so the last worker works longest.
# Better ideas tested here:  (1) many small chunks + imap_unordered   (2) cyclic / interleaved
import time
from multiprocessing import Pool
from primes_common import N, is_prime, count_primes, make_chunks

P = 4


def timed_worker(chunk):                      # returns (count, seconds this worker took)
    t0 = time.perf_counter()
    c = count_primes(*chunk)
    return c, time.perf_counter() - t0


def small_chunk(chunk):
    return count_primes(*chunk)


def cyclic_worker(args):                      # worker i checks i, i+P, i+2P, ...
    start, step = args
    c = 0
    for n in range(start, N + 1, step):
        if is_prime(n):
            c += 1
    return c


def equal_chunks():
    t0 = time.perf_counter()
    with Pool(P) as pool:
        res = pool.map(timed_worker, make_chunks(2, N + 1, P))
    return sum(r[0] for r in res), time.perf_counter() - t0, [r[1] for r in res]


def many_small_chunks(num=64):
    chunks = make_chunks(2, N + 1, num)
    t0 = time.perf_counter()
    with Pool(P) as pool:
        total = sum(pool.imap_unordered(small_chunk, chunks, chunksize=1))
    return total, time.perf_counter() - t0


def cyclic():
    t0 = time.perf_counter()
    with Pool(P) as pool:
        total = sum(pool.map(cyclic_worker, [(2 + i, P) for i in range(P)]))
    return total, time.perf_counter() - t0


if __name__ == "__main__":
    print(f"N = {N}, p = {P}\n")
    # worker times for equal chunks (one run, to show the imbalance)
    cnt, t, wt = equal_chunks()
    print("Equal chunks - time taken by each worker:")
    for i, w in enumerate(wt):
        print(f"  worker {i}: {w:.3f} s")
    print(f"  slowest / fastest = {max(wt) / min(wt):.2f}x\n")

    results = {"equal chunks (p large chunks)": [], "64 small chunks + imap_unordered": [],
               "cyclic / interleaved": []}
    for run in range(3):
        c1, t1, _ = equal_chunks()
        c2, t2 = many_small_chunks()
        c3, t3 = cyclic()
        assert c1 == c2 == c3, "counts differ!"
        results["equal chunks (p large chunks)"].append(t1)
        results["64 small chunks + imap_unordered"].append(t2)
        results["cyclic / interleaved"].append(t3)
    base = sum(results["equal chunks (p large chunks)"]) / 3
    print(f"Count in every design = {c1}  (all correct)\n")
    print(f"{'Design':<36}{'Avg time (s)':>13}{'vs equal chunks':>17}")
    for name, ts in results.items():
        avg = sum(ts) / 3
        print(f"{name:<36}{avg:>13.3f}{(base - avg) / base:>16.0%}")

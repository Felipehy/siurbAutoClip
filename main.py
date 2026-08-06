from multiprocessing import Pool
from orchestrator import Orchestrator

def run_worker(doc_types: list):
    oc = Orchestrator()
    oc.run(doc_types)

def chunk(lst: list, n: int):
    size = len(lst) // n
    return [lst[i * size:(i + 1) * size] for i in range(n - 1)] + [lst[(n - 1) * size:]]

def main():
    listDocs = [1,2,3,4,5,6,7,8,9,10]
    NUM_WORKERS = 3

    chunks = chunk(listDocs, NUM_WORKERS)

    with Pool(processes=NUM_WORKERS) as pool:
        try:
            pool.map(run_worker,chunks)
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
            
if __name__ == "__main__":
    main()

import argparse
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import os
import operator
import time
import threading
import queue
import random
import sys

def utf8len(s):
    return len(s.encode('utf-8'))

class Status(Enum):
    WORKING= 'WORKING'
    SUCCESS= 'SUCCESS'
    TIMEOUT= 'TIMEOUT'
    FAILURE= 'FAILURE'        

class DataGenerator():
    def __init__(self, file_path, max=2000000):
        self.samples = []
        with open(file_path, 'r', encoding="utf-8") as f:
            for line in f:
                for word in line.split(','):
                    self.samples.append(word)
        self.max = max

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n > self.max:
            raise StopIteration
        rand_i = random.randrange(len(self.samples))
        self.n+=1
        return self.samples[rand_i]

class Worker:
    def __init__(self, thread_num : int, timeout : int, result_q : queue.Queue, generator : DataGenerator):
        self.thread_num = thread_num
        self.timeout = timeout
        self.result_q = result_q
        self.generator = generator
        self.interrupt_requested = False

    def interrupt(self):
        self.interrupt_requested = True

    def __call__(self):
        print(f'[Thread-{self.thread_num}]: Started searching...')
        try:
            elapsed = 0
            byte_cnt = 0
            status = Status.WORKING
            target_word = 'FiCo'
            start = time.perf_counter()
            for word in self.generator:
                byte_cnt += utf8len(word)  # some words are lengthier
                
                if self.interrupt_requested:
                    end = time.perf_counter()
                    elapsed = (end - start) * 1000 # return in ms
                    status = Status.TIMEOUT
                    self.result_q.put((self.thread_num, None, None, status.value))
                    print(f'[Thread-{self.thread_num}] TIMEOUT after searching {byte_cnt} bytes {elapsed}ms elapsed.')
                    break

                if word == target_word:
                    end = time.perf_counter()
                    elapsed = (end - start) * 1000 # return in ms
                    status = Status.SUCCESS
                    self.result_q.put((self.thread_num, elapsed, byte_cnt, status.value))
                    print(f'[Thread-{self.thread_num}] Found {target_word} after searching {byte_cnt} bytes {elapsed}ms elapsed.')
                    break
        except:
            e = sys.exc_info()[0]
            sys.stderr.write(e)
            end = time.perf_counter()
            elapsed = (end - start) * 1000 # return in ms
            status = Status.FAILURE
            self.result_q.put((self.thread_num, None, None, status.value))

# User can pass in arguments for timeouts
parser = argparse.ArgumentParser(description='Hatch Takehome Example')
parser.add_argument('--timeout', type=float, default=60, help='Seconds until timeout. (Defaults 60s)')
parser.add_argument('--maxworkers', type=int, default=10, help='Maximum number of workers. (Defaults 10)')
args = parser.parse_args()
timeout = args.timeout
max_workers = args.maxworkers

# generator = DataGenerator('file.txt', 1000000)  # generator to randomly generate 1 Million words
result_q = queue.Queue()

with ThreadPoolExecutor(max_workers=max_workers) as executor:        
    workers = [Worker(i, timeout, result_q, DataGenerator('file.txt', 1000000)) for i in range(max_workers)]
    for worker, future in [(w, executor.submit(w)) for w in workers]:
            try:
                future.result(timeout=timeout)
            except TimeoutError:
                print(f'[Thread-{worker.thread_num}]: TIMEOUT')
                worker.interrupt()


lst_results = list(result_q.queue)
lst_results.sort(key=operator.itemgetter(1, 2, 3), reverse=True)  # sort in descending order of [time elapsed] [bytes_cnt] [status]
total_bytes, total_time = 0,0
for worker_stat in lst_results:
    print(worker_stat)
    if worker_stat[3] == Status.SUCCESS.value:
        total_bytes += worker_stat[2]
        total_time += worker_stat[1]
avg_rate = total_bytes / (total_time / 60)
print(f'Average bytes per second is {avg_rate} ')

    


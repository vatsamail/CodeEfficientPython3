"""
sample line count algorithm to count the number of lines in every file
using MapReduce
python 3 implementation
vatsamail @ github
vatsamail@gmail.com
"""
class InputData(object):
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path, 'rb') as handle:
            return handle.read()

class WorkerBase(object):
    def __init__(self, indata):
        self.ind = indata
        self.result = None
    def map(self):
        raise NotImplementedError
    def reduce(self, other):
        raise NotImplementedError

class LineCountWorker(WorkerBase):
    def map(self):
        data = self.ind.read()
        self.result = data.count(b'\n')

    def reduce(self, other):
        self.result += other.result

import os
def gen_ins(data_dir):
    for file in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, file))

def create_workers(input_list):
    workers = []
    for in_data in input_list:
        workers.append(LineCountWorker(in_data))
    return workers

from threading import Thread
def execute(workers):
    threads = [Thread(target = w.map) for w in workers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first, rest_all = workers[0], workers[1:]
    for worker in rest_all:
        first.reduce(worker)
    return first.result

# glue logic
def map_reduce(data_dir):
    inputs = gen_ins(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

# test case
import random

def write_test_files(tmpdir):
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as handle:
            handle.write('\n' * random.randint(0, 100))

from tempfile import TemporaryDirectory
with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    result = map_reduce(tmpdir)
    print("MapReduce line count results:", result)

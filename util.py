################
# sample function
#################

def to_str(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        raise TypeError('Must be String or Bytes but found %r' % data)

##############
# profiling
##############
from random import randint
from cProfile import Profile
from pstats import Stats

from bisect import bisect_left

def insert_sort(data):
    result = []
    for value in data:
        if value % 2 == 0:
            insert_value_bad(result, value)
        else:
            insert_value_good(result, value)
    return result

def insert_value_good(array, value):
    # only logn time
    i = bisect_left(array, value)
    array.insert(i, value)

def insert_value_bad(array, value):
    # bad algorithm .. as we iterate everytime
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)

max_size = 10 ** 4
data = [randint (0, max_size) for i in range(max_size)]
print("before", data)
result = insert_sort(data)
print("after ", result)

profiler = Profile()
profiler.runcall(lambda: insert_sort(data))
print('Done')
stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


###########################
# stupid functions to burn some CPU time
###########################
from cProfile import Profile
from pstats import Stats

def another_util(a, b):
    c = 1
    for i in range(100):
        c += a * b

def first_func():
    for _ in range(1000):
        another_util(4,5)

def second_func():
    for _ in range(10):
        another_util(1, 3)

def my_program():
    for _ in range(20):
        first_func()
        second_func()

profiler = Profile()
profiler.runcall(my_program)
stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_callers()


################################
# detecting memory leaks
################################
import os
import hashlib

import tracemalloc

tracemalloc.start(10)
time1 = tracemalloc.take_snapshot()

#TODO: to debug .. not working on windows
#import waste_memory
#x = waste_memory.run()

time2 = tracemalloc.take_snapshot()
stats = time2.compare_to(time1, 'lineno')
for stat in stats[:3]:
    print(stat)

class Obj(object):
    def __init__(self):
        self.x = os.urandom(100)
        self.y = hashlib.sha1(self.x).hexdigest()

def get_data():
    values = []

    for _ in range(100):
        obj = Obj()
        values.append(obj)


def run():
    deep_values = []
    for _ in range(100):
        deep_values.append(get_data())
    return deep_values
a = Obj()
print("A", a.x, a.y)
print(run())

import gc # garbage colector
found_obj = gc.get_objects()
print('%d objects before' % len(found_obj))


found_obj = gc.get_objects()
print('%d objects after' % len(found_obj))

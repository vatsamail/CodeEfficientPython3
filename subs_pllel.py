"""
learning threading and subprocess
 on a windows machine
python 3 implementation
vatsamail @ github
vatsamail@gmail.com
"""
import subprocess
proc = subprocess.Popen(
        ['dir', '..\\'],
        stdout=subprocess.PIPE
    )
out, err = proc.communicate()
print(out.decode('utf-8'))

################
import time
proc = subprocess.Popen(['sleep', '0.3'])
while proc.poll() is None:
    print('working')
    # time comsuming work goes here
    time.sleep(0.1)
print("Exit status", proc.poll())

######################

def run_sleep_work(name, period):
    proc = subprocess.Popen(['sleep', str(period)])
    print(name)
    return proc

start = time.time()
procs = []
for i in range(10):
    proc = run_sleep_work(str(i), 0.1)
    procs.append(proc)

for proc in procs:
    proc.communicate()
end = time.time()
print('Total time was %.3f seconds' % (end - start))

#######################
import os
import subprocess
def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'asdf'
    for e in env.keys():
        print(e,'=>', env[e])
        env[e] = str(e)

    proc = subprocess.Popen(
            ['openssl', 'enc', '-des3', '-pass', 'env:password'],
            env=env,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc

#TODO remove me
#proc = run_openssl(b'blah')
print(proc)
out, _ = proc.communicate()
print(out)

#####################
proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print("Exit status", proc.poll())
#################
# using threads
#################

def factorize(number):
    for i in range(1, number+1):
        if number % i == 0:
            yield i

print("21 factors", list(factorize(21)))
#nums = [215345, 50123432, 4546312] # the real challenging one
nums = [1, 2, 4]
import time

start = time.time()
for n in nums:
    obj = factorize(n)
    print('\n')
    for i in obj:
        print(i, "is a factor of ", n)
end = time.time()
print("Time consumed %.3f seconds" % (end - start))


import threading
class FactorizeThread(threading.Thread):
    def __init__(self, number):
        super().__init__()
        self.num = number

    def run(self):
        self.factors = list(factorize(self.num))

thread = FactorizeThread(21)
thread.start()
thread.join()
print(thread.factors)

threads = []
start = time.time()
for n in nums:
    thread = FactorizeThread(n)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
    print('Factors %r' % (thread.factors))
end = time.time()
print("Thread computation time in %.3f seconds"% (end - start))

#############################
import socket
import select
import subprocess
def slow_syscall():
    pass
    #TODO doesn't work on windows even after importing socket!
    #select.select([3],[],[]) # wait 0.1 seconds
    proc = subprocess.Popen(['sleep', '0.1'])

start = time.time()
for i in range(5):
    slow_syscall()
end = time.time()
print("System call time in %.3f seconds"% (end - start))


#######################
# using locks
#######################
import threading
import random

class Counter(object):
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()

    def increase(self, count):
        #self.counter += count
        with self.lock:
            self.counter += count


worker_count = 5
barrier = threading.Barrier(worker_count)

def worker(sensor_data, how_many_counterm, counter_obj):
    barrier.wait() # once we wait for all the threads on the barrier
    for _ in range(how_many_counterm):
        val = random.randint(0, 100)
        counter_obj.increase(1) # you can write 'val' to add more drama to the code

threads = []
counter = Counter()
how_many = 100 # if you increase it to 10000000 .. things will get inaccurate

for i in range(worker_count):
    args = (1, how_many, counter)
    thread = threading.Thread(target=worker, args=args)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
    print(counter.counter)

print("Global Counter value:", counter.counter)

###########
# using queues to coordinate between locks
###########
#import queue
from queue import Queue
import threading
import time
q_buffer_size = 3
queue = Queue(q_buffer_size)
def consumer(items):

    print("Consumer waiting")
    for i in range(items):
        time.sleep(0.1)
        queue.get()
        queue.task_done()
        print("Consumer catered %d item" % i)


items = 10
thread = threading.Thread(target=consumer, args=(items,))
thread.start()

print("Producer started adding")
for i in range(items):
    print("Producer added %d item" % i)
    queue.put(object())
thread.join()
print("Producer finished")


#################
# queue  and threads in class
################
from queue import Queue
from threading import Thread
import time

class ClosableQueue(Queue):
    SOMEOBJ = object()

    def close(self):
        self.put(self.SOMEOBJ)

    def __iter__(self):
        # allow you to iter on the object
        while True:
            item = self.get()
            try:
                if item is self.SOMEOBJ:
                    return
                yield item
            finally:
                self.task_done()

class StoppableWorker(Thread):

    def __init__(self, func, inq, outq):
        super().__init__()
        self.func = func
        self.inq = inq
        self.outq= outq

    def run(self):
        for item in self.inq:
            result = self.func(item)
            self.outq.put(item)

"""
usecase scenario: download from camera, resize the image and upload to the net
"""

def download(item):
    # faking download from DSLR time
    time.sleep(0.1)
    print("downloading", item)
    return item

def resize(item):
    # faking resizing the image on the sloppy computer
    time.sleep(0.2)
    print("resizing", item)
    return item

def upload(item):
    # faking the upload the resized images on google drive through high speed internet
    time.sleep(0.05)
    print("uploading", item)
    return item

queue_size = 10
download_q = ClosableQueue(10)
resize_q = ClosableQueue(10)
upload_q = ClosableQueue(10)
done_q = ClosableQueue()

threads = [
    StoppableWorker(download, download_q, resize_q),
    StoppableWorker(resize, resize_q, upload_q),
    StoppableWorker(upload, upload_q, done_q),
]

for thread in threads:
    thread.start()

for i in range(10): # 1000 photos
    download_q.put("photo_"+str(i))

download_q.close()
download_q.join() # wait until the task done (into resize q)
resize_q.close()
resize_q.join()
upload_q.close()
upload_q.join()

print("Photos processed:", done_q.qsize())

######################
# computationally intensive parallelism
#########################
import time
from concurrent.futures import ThreadPoolExecutor
#from concurrent.futures import ProcessPoolExecutor
def gcd(pair):
    a,b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a%i == 0 and b%i == 0:
            return i
    return 1

print("gcd", gcd((54, 12)) )

start = time.time()

#ThreadPoolExecutor will not improve exec time
pool = ThreadPoolExecutor(max_workers=2) # no of CPUs on the computer

#ProcessPoolExecutor will improve exec time!
#pool = ProcessPoolExecutor(max_workers=2) # no of CPUs on the computer

nums = [(1124454,22878), (231134, 22268), (1235766, 32532543393)]
results = list(map(gcd, nums)) # normal way
results = list(pool.map(gcd, nums))
end  = time.time()
print("Time taken to run gcd is %.4f" % (end - start), 'seconds', "for the inputs", nums, "results are", results)

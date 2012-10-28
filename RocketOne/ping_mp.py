# example for article http://proft.com.ua/parallelizm-v-python/
import time
import multiprocessing
import Queue
import subprocess

ips = ['proft.com.ua', 'google.com', 'ua.pycon.org', 'habrahabr.ru', 'ya.ru', 'ubuntu.com', 'centos.org', 'ru.wikipedia.org']

def processing(thread_num, iq):
    while True:
        ip = iq.get()

        r = subprocess.call("ping -c 1 %s" % ip, shell=True, stdout=open("/dev/null", "w"), stderr=subprocess.STDOUT)
        if r == 0:
            print "%s: is alive" % ip
        else:
            print "%s: did not respond" % ip

        iq.task_done()

num_process = 4
in_queue = multiprocessing.JoinableQueue()

t_start_fill = time.time()

for ip in ips:
    in_queue.put(ip)

t_start_calc = time.time()

for i in xrange(num_process):
    worker = multiprocessing.Process(target=processing, args=(i, in_queue))
    worker.daemon = True
    worker.start()

in_queue.join()

t_end = time.time()

print "*"*20
print t_end - t_start_fill
print t_end - t_start_calc

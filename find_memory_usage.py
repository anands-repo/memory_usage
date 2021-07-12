import psutil
import os
import subprocess
import sys
import time
import logging

logging.basicConfig(level=logging.INFO)


def get_recursive_sum(proc):
    try:
        return proc.memory_info().rss + sum(get_recursive_sum(c) for c in proc.children())
    except psutil.NoSuchProcess:
        return 0


def get_recursive_cpu(proc):
    try:
        return proc.cpu_percent(1) + sum(get_recursive_cpu(c) for c in proc.children())
    except psutil.NoSuchProcess:
        return 0


if len(sys.argv) != 2:
    logging.info("Usage: python %s <shell script>" % sys.argv[0])
    sys.exit()

command = sys.argv[1]
pid_line = None

process = subprocess.Popen(["bash", sys.argv[1]])
proc = psutil.Process(process.pid)
max_memory = 0
max_cpu = 0

while process.poll() is None:
    current_memory = get_recursive_sum(proc)
    current_cpu = get_recursive_cpu(proc)
    max_memory = max(max_memory, current_memory)
    max_cpu = max(max_cpu, current_cpu)
    logging.info("Max, current memory = %d, %d" % (max_memory, current_memory))
    logging.info("Max, current cpu = %f, %f" % (max_cpu, current_cpu))
    time.sleep(5)

logging.info("Completed running the command, maximum memory is %d bytes, cpu usage is %f" % (max_memory, max_cpu))

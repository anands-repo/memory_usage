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


if len(sys.argv) != 2:
    logging.info("Usage: python %s <shell script>" % sys.argv[0])
    sys.exit()

command = sys.argv[1]
pid_line = None

process = subprocess.Popen(["bash", sys.argv[1]])
proc = psutil.Process(process.pid)
max_memory = 0

while process.poll() is None:
    current_memory = get_recursive_sum(proc)
    max_memory = max(max_memory, current_memory)
    logging.info("Max, current memory = %d, %d" % (max_memory, current_memory))
    time.sleep(2)

logging.info("Completed running the command, maximum memory is %d bytes" % max_memory)

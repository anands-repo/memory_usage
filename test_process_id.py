import psutil
import subprocess
import random
import time


def get_pid_from_ps(filename):
    pid_line = None

    while pid_line is None:
        with open("/tmp/ps_command%d.txt" % random.randint(0, 32000), "w") as fhandle:
            logname = fhandle.name
            subprocess.call(["ps", "-ef"], stdout=fhandle)
    
        with open(logname, "r") as fhandle:
            for line in fhandle:
                if filename in line:
                    pid_line = line
                    print("PID line = %s" % pid_line)
                    break
    
        time.sleep(2)
    
    pid = int(line.split()[1])
    
    print("Process id = %d" % pid)

    return pid


with open("/tmp/a_random_test_case%d.sh" % random.randint(0, 32000), "w") as fhandle:
    filename = fhandle.name
    fhandle.write("sleep 10")

process = subprocess.Popen(["bash", filename])

pid_from_popen = process.pid
pid_from_ps = get_pid_from_ps(filename)

print("PID from Popen = %d" % pid_from_popen)
print("PID from ps = %d" % pid_from_ps)

assert(pid_from_popen == pid_from_ps), "PID mismatch!"

while process.poll() is None:
    print("Waiting for process to be over ... ")
    time.sleep(3)

print("Test passed")


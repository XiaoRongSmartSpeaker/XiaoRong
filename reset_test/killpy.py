import os
import subprocess
from subprocess import Popen, PIPE

def get_pname(pid):
    p1 = Popen(["ps", "-p", str(pid), "--no-headers" ,"-o", "cmd"], stdout=PIPE)
    p2 = Popen(["awk" ,"{ print $NF }"], stdin=p1.stdout, stdout=PIPE)
    return str(p2.communicate()[0])

pGetPid = Popen(['ps', '-A'], stdout=PIPE)
output, error = subprocess.communicate()

target_process = "python"
for line in output.splitlines():
    if target_process in str(line):
        pid = int(line.split(None, 1)[0])
        pname = get_pname(pid)
        print(pname)
        if pname != "b'killpy.py\\n'": 
            os.kill(pid, 9)
import os
import subprocess

def get_pname(pid):
    process = subprocess.Popen([f"ps -p {pid} --no-headers -o cmd | awk '{{ print $NF }}'"])
    return str(process.communicate()[0])

subprocess = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
output, error = subprocess.communicate()

target_process = "python"
for line in output.splitlines():
    if target_process in str(line):
        pid = int(line.split(None, 1)[0])
        print(get_pname(pid))
        os.kill(pid, 9)
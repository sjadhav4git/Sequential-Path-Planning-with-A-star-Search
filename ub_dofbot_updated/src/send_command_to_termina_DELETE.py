import subprocess
command = 'ls'

process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

stdout, stderr= process.communicate()

print("std_out")
print(stdout.decode())
print("\nstd_error")
print(stderr.decode())
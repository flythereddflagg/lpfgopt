import os
import time

start = time.time()
print "\nrunning command: nuitka --standalone lpfg_0_5_2.py\n"
print "Time start...",
os.system("nuitka --standalone lpfg_0_5_2.py")
stop = time.time() - start
print "Done."
print "\nTime to compile to standalone: %s sec\n" % stop

from pathlib import Path
import sys
import subprocess
import os
cwd = Path(os.getcwd())
parent = cwd.parent.absolute()
process = subprocess.Popen([sys.executable, "crappyproxy.py"], cwd=parent)
pid1 = process.pid
#import os
e = 'psrecord '+str(pid1)+' --interval .5 --plot plot1.png' 
print('Executing: '+e)
os.system(e)
#cwd = Path(os.getcwd())
#parent = cwd.parent.absolute()

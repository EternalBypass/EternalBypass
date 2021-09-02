import datetime
today = datetime.date.today()
weekday = today.weekday()
import time

if (weekday == 0):
    start = time.time()
    print('Clearing cache.')
    import os
    with open("currentTempDirs", "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            os.system('rm -rf '+stripped_line)
    f = open('currentTempDirs', 'w')
    f.flush()
    f.close()
    end = time.time()
    print('Finished in '+str(end-start)+' seconds.')

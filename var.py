import time
import sys


def animate():
    for i in range(0, 2):
        sys.stdout.write('\rChecking through the rows.')
        time.sleep(0.35)
        sys.stdout.write('\rChecking through the rows..')
        time.sleep(0.35)
        sys.stdout.write('\rChecking through the rows...')
        time.sleep(0.35)


animate()

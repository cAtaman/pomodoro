#!/usr/bin/env python3
import sys
import time
import subprocess


def timer(no_sess, work_prd, short_brk, long_brk):
    for sess in range(1, no_sess+1):
        alert(f'Session {sess} started')
        time.sleep(work_prd)
        if sess != no_sess:
            alert(f'Break {sess}')
            time.sleep(short_brk)
        else:
            alert('Long break')
            time.sleep(long_brk)
    alert('Long break complete')

      
def alert(msg):
    subprocess.run([
        "notify-send",
        "--hint=string:sound-name:system-ready",
        "Pomodoro",
        msg,
    ])
    return True


def parse_args():
    defaults = [4, 25, 5, 15]
    reps = 0
    args = sys.argv[1:]
    if (not args) or ("-h" in args) or ("--help" in args):
        print(' Use "pomodoro [options] [no_sess] [work_prd] [short_brk] [long_brk]"')
        print(' arguments are in minutes (except no_sess)')
        print('\n options')
        print(' -d            use default values: 4, 25, 5, 15')
        print(' -r [n <int>]  to repeat the timer for "n" times; by default it repeat infinitely')
        print(' -h, --help    displays this help menu')
        print()
        sys.exit()
    if "-r" in args:
        idx = args.index("-r")
        reps = int(args.pop(idx+1))
        args.remove("-r")
    if "-d" in args:
        args.remove("-d")
        val = defaults
    elif len(args) == 4:
        val = list(map(int, args))
    else:
        print('INFO: You must supply values for the time or use default "-d"')
        print('      see usage information with `pomodoro -h`')
        print()
        sys.exit()    
    return reps, val


def main():
    reps, val = parse_args()
    val = [val[0]] + list(map(lambda x: 60*x, val[1:]))
    count = 0
    while True:
        timer(*val)
        count += 1
        if (reps > 0) and count == reps:
            break
    alert('{} session{} completed'.format(count, ["", "s"][count>1]))


if __name__ == '__main__':
    main()

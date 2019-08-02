#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-----------------------------------------------------------------------------------------------------------
# Name:         01ThreadCounter.py
# Purpose:      Simple thread counter
#
# Author:       Gabriel Marti Fuentes
# email:        gabimarti at gmail dot com
# GitHub:       https://github.com/gabimarti
# Created:      02/08/2019
# License:      MIT
#-----------------------------------------------------------------------------------------------------------
#

import argparse
import random
import threading
import time

########################################################
# CONSTANTS
########################################################
DESCRIPTION = 'A simple thread counter'
EPILOG = 'What do you want me to tell you?'
MAXTHREADS = 10000
VERBOSE_LEVELS = [ "none", "a few", "insane info" ]                     # Verbose levels description
MAXRANDOM = 10                                                          # Max time for random sleep

########################################################
# VARIABLES
########################################################
thread_counter = 0                                                      # Total executed threads
thread_active_counter = 0                                               # Number of current active threads
thread_list = []                                                        # List of active threads
verbose = 0                                                             # verbose level

########################################################
# FUNCTIONS
########################################################

# Wait a random time
def do_something_more(thread_id, thread_active_counter, max_random):
    seconds = random.randint(1, max_random)
    if verbose == 2:
        print("Thread id %d : Active counter %d : Random Sleep %d" % (thread_id, thread_active_counter, seconds))
    time.sleep(seconds)


# Increase counters and call auxiliary function
def do_something(thread_id, max_random):
    global thread_counter, thread_active_counter

    thread_counter += 1
    thread_active_counter += 1
    do_something_more(thread_id, thread_active_counter, max_random)
    thread_active_counter -= 1


# Parse command line parameters
def parse_params():
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("-m", "--maxthreads", type=int, default=MAXTHREADS,
                        help="Indicates the maximum number of threads. Default value: " + str(MAXTHREADS))
    parser.add_argument("-v", "--verbose", type=int, choices=[0, 1, 2], default=0,
                        help="Increase output verbosity. Default value: 0")
    args = parser.parse_args()
    return args


def main():
    global verbose

    # Check and parse parameters
    args = parse_params()
    verbose = args.verbose

    print("Verbose level "+str(VERBOSE_LEVELS[verbose]))
    print("Max Threads "+str(args.maxthreads))
    print("Launching ...")
    start = time.perf_counter()

    # Launch threads
    for t_id in range(1, int(args.maxthreads)+1):
        thread_handler = threading.Thread(target=do_something, args=(t_id, MAXRANDOM))
        thread_handler.start()
        thread_list.append(thread_handler)

    print("Finished threads launch.")
    print("Total threads %d : Current active %d" % (thread_counter, thread_active_counter))
    # Wait to finish threads
    for thread_wait in thread_list:
        thread_wait.join()

    totaltime = time.perf_counter() - start
    print("Performed %d threads in %6.2f seconds " % (thread_counter, totaltime))

if __name__ == '__main__':
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-----------------------------------------------------------------------------------------------------------
# Name:         02Template.py
# Purpose:      This is a copy of 01ThreadCounter.py
#               saved as a template for other modules
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
DELAYBETWEENTHREADS = 0                                                 # Milliseconds of delay between threads
VERBOSE_LEVELS = [ "basic", "a few", "insane info" ]                    # Verbose levels description
MAXRANDOMSLEEP = 10                                                     # Max time in seconds for random sleep


########################################################
# VARIABLES
########################################################
thread_counter = 0                                                      # Total executed threads
thread_active_counter = 0                                               # Number of current active threads
thread_list = []                                                        # List of active threads
max_threads = MAXTHREADS                                                # Max threads
verbose = 0                                                             # Verbose level
delay_threads = DELAYBETWEENTHREADS                                     # Delay between threads
max_random_sleep = MAXRANDOMSLEEP                                       # Max random sleep


########################################################
# FUNCTIONS
########################################################

# Wait for the indicated time in milliseconds
def delay_miliseconds(milisec):
    if milisec == 0:
        return None                     # Avoid making unnecessary call to time.sleep function
    time.sleep(milisec/1000)


# Wait a random time
def do_something_more(thread_id, max_random_sleep, verbose):
    global thread_active_counter

    seconds = random.randint(0, max_random_sleep+1)
    if verbose >= 2:
        print("Begin thread id %d : Active counter %d : Random Sleep %d" % (thread_id, thread_active_counter, seconds))
    time.sleep(seconds)
    if verbose >= 2:
        print("End thread id %d : Active counter %d " % (thread_id, thread_active_counter))


# Increase counters and call auxiliary function
def do_something(thread_id, max_random_sleep, verbose):
    global thread_counter, thread_active_counter

    thread_counter += 1
    thread_active_counter += 1
    do_something_more(thread_id, max_random_sleep, verbose)
    thread_active_counter -= 1


# Parse command line parameters
def parse_params():
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("-m", "--maxthreads", type=int, default=MAXTHREADS,
                        help="Indicates the maximum number of threads. Default value: " + str(MAXTHREADS))
    parser.add_argument("-d", "--delay", type=int, default=DELAYBETWEENTHREADS,
                        help="Milliseconds of delay between threads call. Default value: " + str(DELAYBETWEENTHREADS))
    parser.add_argument("-v", "--verbose", type=int, choices=[0, 1, 2], default=0,
                        help="Increase output verbosity. Default value: 0")
    args = parser.parse_args()
    return args


# Main
def main():
    global max_threads, delay_threads, verbose, max_random_sleep

    # Check and parse parameters
    args = parse_params()
    verbose = args.verbose
    max_threads = args.maxthreads
    delay_threads = args.delay
    max_random_sleep = MAXRANDOMSLEEP

    print("Verbose level "+str(VERBOSE_LEVELS[verbose]))
    print("Max %d Threads " % (max_threads))
    print("Delay between Threads %d milliseconds" % (delay_threads))
    print("Launching ...")
    start = time.perf_counter()

    # Launch threads and execute function do_something()(
    for t_id in range(1, int(max_threads)+1):
        thread_handler = threading.Thread(target=do_something, args=(t_id, max_random_sleep, verbose))
        thread_handler.start()
        thread_list.append(thread_handler)
        delay_miliseconds(delay_threads)                # delay between threads

    if verbose >= 1:
        print("Finished threads launch.")
        print("Total threads %d : Current active %d" % (thread_counter, thread_active_counter))
        partialtime = time.perf_counter() - start
        print("Launched %d threads in %6.2f seconds " % (thread_counter, partialtime))

    # Wait to finish threads
    for thread_wait in thread_list:
        thread_wait.join()

    totaltime = time.perf_counter() - start
    print("Performed %d threads in %6.2f seconds " % (thread_counter, totaltime))
    print("Current active threads %d" % (thread_active_counter))


if __name__ == '__main__':
    main()


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
# Revision:     02/08/2019  by foratnegre  :    Some improvements in the code.
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
VERBOSE_LEVELS = ['basic', 'a few', 'insane info']                      # Verbose levels description
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
total_sleep_seconds = 0                                                 # Total seconds of sleep performed
average_sleep = 0                                                       # Average sleep executed


########################################################
# FUNCTIONS
########################################################

# Wait for the indicated time in milliseconds
def delay_milliseconds(millisec):
    if millisec == 0:
        return None                     # Avoid making unnecessary call to time.sleep function
    time.sleep(millisec/1000)


# Wait a random time
def do_something_more(thread_id, max_random_sleep, verbose):
    global thread_counter, total_sleep_seconds

    seconds = random.randint(0, max_random_sleep+1)
    total_sleep_seconds += seconds
    if verbose ==1:
        print('.', end='')
        
    if verbose >= 2:
        print('Begin thread id %d : Active counter %d : Random Sleep %d' % (thread_id, thread_active_counter, seconds))
    time.sleep(seconds)
    if verbose >= 2:
        print('End thread id %d : Active counter %d ' % (thread_id, thread_active_counter))


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
    parser.add_argument('-m', '--maxthreads', type=int, default=MAXTHREADS,
                        help='Indicates the maximum number of threads. Default value: ' + str(MAXTHREADS))
    parser.add_argument('-d', '--delay', type=int, default=DELAYBETWEENTHREADS,
                        help='Milliseconds of delay between threads call. Default value: ' + str(DELAYBETWEENTHREADS))
    parser.add_argument('-s', '--randomsleep', type=int, default=MAXRANDOMSLEEP,
                        help='Max random sleep in seconds for every process. Default value: ' + str(MAXRANDOMSLEEP))
    parser.add_argument('-v', '--verbose', type=int, choices=[0, 1, 2], default=0,
                        help='Increase output verbosity. Default value: 0')
    args = parser.parse_args()
    return args


def main():
    global max_threads, delay_threads, verbose, max_random_sleep

    # Check and parse parameters
    args = parse_params()
    verbose = args.verbose
    max_threads = args.maxthreads
    delay_threads = args.delay
    max_random_sleep = args.randomsleep

    if max_threads < 1:         # avoid zero division
        max_threads = 1

    print('Verbose level '+str(VERBOSE_LEVELS[verbose]))
    print('Max %d Threads ' % (max_threads))
    print('Delay between Threads %d milliseconds' % (delay_threads))
    print('Max random Sleep for every process %d seconds' % (max_random_sleep))
    print('Launching ...')
    start = time.perf_counter()

    # Launch threads and execute function do_something()(
    for t_id in range(1, int(max_threads)+1):
        thread_handler = threading.Thread(target=do_something, args=(t_id, max_random_sleep, verbose))
        thread_handler.start()
        thread_list.append(thread_handler)
        delay_milliseconds(delay_threads)               # delay between threads

    if verbose >= 1:
        print('Finished threads launch.')
        print('Total threads %d : Current active %d' % (thread_counter, thread_active_counter))
        partialtime = time.perf_counter() - start
        print('Launched %d threads in %6.2f seconds ' % (thread_counter, partialtime))

    # Wait to finish threads
    for thread_wait in thread_list:
        thread_wait.join()

    totaltime = time.perf_counter() - start
    average_sleep = total_sleep_seconds / thread_counter
    print('Performed %d threads in %6.2f seconds ' % (thread_counter, totaltime))
    print('Current active threads %d' % (thread_active_counter))
    print('Total sleep %d (shared) seconds for all process' %(total_sleep_seconds))
    print('Average sleep %6.2f seconds' % (average_sleep))


if __name__ == '__main__':
    main()


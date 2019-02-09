#!/bin/env python3
import time
from threading import Thread
from TwitchOnlineChecker import *


THREAD_LOOP_DELAY = 0.5


class AsyncRecurringJob(Thread):
    runningJobs = dict()
    def __init__(self, function, period):
        Thread.__init__(self)
        self.starting_point = time.time()
        self.period = period
        self.callback = function
        self.should_stop = False

        AsyncRecurringJob.runningJobs[len(AsyncRecurringJob.runningJobs)] = self


    def run(self):
        while not self.should_stop:
            current = time.time()
            if self.starting_point + self.period <= current:
                self.starting_point = current
                self.callback()
            time.sleep(THREAD_LOOP_DELAY)


    @staticmethod
    def launchlastjob():
        AsyncRecurringJob.runningJobs[len(AsyncRecurringJob.runningJobs) - 1].start()


class AsyncDelayedJob(Thread):
    def __init__(self, function, delay):
        Thread.__init__(self)
        self.starting_point = time.time()
        self.delay = delay
        self.callback = function

    def run(self):
        while True:
            current = time.time()
            if self.starting_point + self.delay <= current:
                self.starting_point = current
                self.callback()
        time.sleep(THREAD_LOOP_DELAY)


def cleanup():
    for j in AsyncRecurringJob.runningJobs.values():
        j.should_stop = True


def create_job_twitch_checker(task, delay):
    def twch():
        TwitchOnlineChecker([task]) # -c -a --name etc.

    AsyncRecurringJob(twch, delay)
    AsyncRecurringJob.launchlastjob()


def parse(args):
    if args[0].lower() == 'createjob':
        if args[1].lower() == 'twitchchecker':
            print('>>> Creating twitch job with ', args[3:])
            create_job_twitch_checker(''.join(args[3:]), int(args[2]))

    if args[0].lower() == 'execute':
        if args[1].lower() == 'twitchchecker':
            TwitchOnlineChecker(''.join(args[2:]))


def main():
    while True:
        inp = input(">>>")
        args = inp.split()
        try:
            parse(args)
        except IndexError:
            pass

        if len(args) > 0:
            if args[0] == 'exit':
                break



    cleanup()


if __name__ == '__main__':
    main()

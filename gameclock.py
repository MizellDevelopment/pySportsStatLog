import time
import threading


class GameClock:
    """ GameClock to keep track of the time and period of a game

    The clock can be Started, Stopped, and Changed. Start creates a new thread to run the clock.
    The run clock handler creates a new thread to sleep during the time intervals and wait for when
    to alter the clock. This allows for the clock to be started and stopped quickly without using the
    CPU and also without waiting between sleep time intervals.

    After initializing the clock it should only be altered with the methods or clock_time read.
    """

    def __init__(self, clock_accuracy=1):
        self.clock_time = 0
        self._clock_accuracy = clock_accuracy
        self._clock_run_num = 0
        self._clock_status = 'stopped'
        self._clock_event = threading.Event()
        self._clock_lock = threading.Lock()
        self.game_period = 1

    def check_clock_status(self):
        if self._clock_status not in ['stopped', 'running']:
            wrong_clock_status = self._clock_status
            self._clock_status = 'stopped'
            raise ValueError('Clock status was not an accepted value: ' + wrong_clock_status)

    def start_clock(self):
        self.check_clock_status()
        if self._clock_status == 'stopped':
            run_thread = threading.Thread(target=self.run_clock)
            run_thread.daemon = True
            run_thread.start()

    def stop_clock(self):
        self.check_clock_status()
        if self._clock_status == 'running':
            self._clock_status = 'stopped'
            self._clock_event.set()

    def change_clock(self, set_clock_time):
        self.stop_clock()
        self._clock_lock.acquire()
        self.clock_time = set_clock_time
        self._clock_lock.release()

    def sleep_clock(self, sleep_run_num):
        target_add = 0
        sleep_start_time = time.time()
        while self._clock_status == 'running':
            target_add += self._clock_accuracy
            time.sleep((sleep_start_time + target_add) - time.time())
            if sleep_run_num == self._clock_run_num and not self._clock_event.is_set():
                self._clock_event.set()
            else:
                break

    def run_clock(self):
        self._clock_run_num += 1
        thread_run_num = self._clock_run_num
        if self._clock_event.is_set():
            self._clock_event.clear()

        self._clock_lock.acquire()
        self._clock_status = 'running'
        run_sleep = threading.Thread(target=self.sleep_clock, args=(thread_run_num,))
        run_sleep.daemon = True
        run_sleep.start()

        while True:
            self._clock_event.wait()
            if self._clock_status == 'running' and thread_run_num == self._clock_run_num:
                self._clock_event.clear()
                self.clock_time += self._clock_accuracy
            else:
                self._clock_lock.release()
                break

    def change_game_period(self, period_change, clock_change=0):
        self.change_clock(clock_change)
        self.game_period = self.game_period + period_change


if __name__ == '__main__':
    pass

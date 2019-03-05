import gameclock
import time


# Test Initialing
def test_init():
    clocking_test = gameclock.GameClock()
    assert clocking_test.clock_time == 0
    assert clocking_test._clock_run_num == 0
    assert clocking_test._clock_status == 'stopped'
    assert clocking_test.game_period == 1
    assert clocking_test._clock_accuracy == 1


# Test starting clock and letting it run for 3 seconds and stopping clock
def test_3sec_run_and_stop():
    clocking_test = gameclock.GameClock()
    clocking_test.start_clock()
    time.sleep(3.1)
    assert clocking_test.clock_time == 3
    clocking_test.stop_clock()
    time.sleep(1)
    assert clocking_test.clock_time == 3


# Test changing clock time
def test_change_clock():
    clocking_test = gameclock.GameClock()
    clocking_test.change_clock(100)
    assert clocking_test.clock_time == 100
    clocking_test.start_clock()
    time.sleep(3.1)
    assert clocking_test.clock_time == 103


# Test changing clock accuracy
def test_clock_accuracy():
    clocking_test = gameclock.GameClock(.25)
    clocking_test.start_clock()
    time.sleep(0.85)
    clocking_test.stop_clock()
    assert clocking_test.clock_time == 0.75


# Test starting and stopping clock quickly
def test_quick_start_and_stop():
    clocking_test = gameclock.GameClock(2)
    clocking_test.start_clock()
    time.sleep(1)
    test_time = time.time()
    clocking_test.change_clock(100)
    assert (time.time() - test_time) < .1
    clocking_test.start_clock()
    time.sleep(2.1)
    clocking_test.stop_clock()
    time.sleep(1)
    assert clocking_test.clock_time == 102

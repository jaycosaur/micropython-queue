# micropython-queue

A simple micropython re-implementation of the threading.Queue class.

Note that this requires the \_thread module of micropython.

## differences from standard python threading.Queue

Please note that there is a fundamental difference as the current implementation stands. Puts and gets do not wait for items on the queue and return after the lock is acquired. The timeouts for the put and get methods relate to timeouts on the lock acquisition unlike the standard module which is the timeout for waiting for new items on the queue / a spot to appear on the queue.

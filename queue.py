# Simple implementation of the threading.Queue module found in the python stand library
# for use with the micro-python _thread module

# does not implement the same method for put as threading.Queue module
# *timeout here implies the max wait time for acquiring the lock

import _thread


class Full(Exception):
    pass


class Empty(Exception):
    pass


class Queue:
    def __init__(self, maxsize=0):
        # something
        self.queue = []
        self.lock = _thread.allocate_lock()
        self.maxsize = maxsize

    def _add_item_to_queue_if_ok(self, item):
        if self.maxsize == 0 or len(self.queue) <= self.maxsize:
            self.queue.append(item)
        else:
            raise Full('The queue is full.')

    def _pop_first(self):
        try:
            item = self.queue.pop(0)
        except IndexError:
            raise Empty('No items are in the queue.')

        return item

    def put(self, item, block=True, timeout=None):
        # acquire lock
        lock_success = self.lock.acquire(
            1 if block else 0, -1 if not timeout else timeout)
        try:
            if lock_success:
                self._add_item_to_queue_if_ok(item)
        finally:
            # release lock
            self.lock.release()

    def put_nowait(self, item):
        self.put(item, False)

    def get(self, block=True, timeout=None):
        lock_success = self.lock.acquire(
            1 if block else 0, -1 if not timeout else timeout)
        try:
            if lock_success:
                item = self._pop_first()
        finally:
            # release lock
            self.lock.release()
        return item

    def get_nowait(self):
        return self.get(False)

    def empty(self):
        # does not acquire lock
        return len(self.queue) == 0

    def full(self):
        # does not acquire lock
        if self.maxsize == 0:
            return False
        return len(self.queue) == self.maxsize

    def qsize(self):
        # does not acquire lock
        return len(self.queue)

import time
import threading

class EasyDict:
    def __init__(self, data: dict):
        self._dict = data

    def update(self, data):
        self._dict.update(data)

    def __iter__(self):
        return self._dict.__iter__()

    def __setattr__(self, attrname, value):
        if attrname == '_dict':
            return super(EasyDict, self).__setattr__(attrname, value)

        self._dict[attrname] = value

    def __getattr__(self, attrname):
        if attrname in self._dict:
            attvalue = self._dict[attrname]
            if isinstance(attvalue, dict):
                return EasyDict(attvalue)
            else:
                return attvalue

        return None

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        return self.__setattr__(key, value)

    def __repr__(self):
        return str(self._dict)


class TypeHandler(object):
    def __init__(self):
        self._handler_dict = {}
        
    def handle(self, data_type):
        if data_type in self._handler_dict:
            return self._handler_dict[data_type]
        elif 'default' in self._handler_dict:
            return self._handler_dict['default']
        else:
            raise NotImplementedError(f'handler of type "{data_type}" not implemented')

    def type(self, data_type):
        def wrapper(func):
            self._handler_dict[data_type] = func
            return func
        return wrapper


class ThreadPool:
    def __init__(self, num_threads=8, daemon_mode=False):
        self._max_threads = num_threads
        self._threads = []
        self._daemon_mode = daemon_mode

    def _num_threads_alive(self):
        i = 0
        while i < len(self._threads):
            t = self._threads[i]
            if t.is_alive():
                i += 1
            else:
                self._threads.pop(i)

        return len(self._threads)

    def map(self, target, jobs):
        self._total = len(jobs)
        for i in range(self._total):
            job = jobs[i]
            if not isinstance(job, (tuple, list)):
                job = (job, )

            thread = threading.Thread(target=target, args=job)
            self._threads.append(thread)
            thread.setDaemon(self._daemon_mode)
            thread.start()

            while self._num_threads_alive() >= self._max_threads:
                time.sleep(0.01)

        while self._num_threads_alive():
            time.sleep(0.01)
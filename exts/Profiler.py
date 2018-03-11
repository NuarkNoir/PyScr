import time


class Profiler(object):
    def usage(self):
        print("with Profiler() as p:\n\t#your code here")

    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))
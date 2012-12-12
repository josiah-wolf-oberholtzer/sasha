import multiprocessing


class PeakDetectionWorker(multiprocessing.Process): 

    def __init__(self, task_queue, result_queue, **kwargs):
        multiprocessing.Process.__init__(self)

        self.task_queue = task_queue
        self.result_queue = result_queue
        self.kwargs = kwargs

    def run(self):
        proc_name = self.name
        while True:
            task = self.task_queue.get()
            if task is None:
                # poison pill causes worker shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s: %s %d' % (proc_name, task, task.offset)
            task(**self.kwargs)
            self.task_queue.task_done()
            self.result_queue.put(task)
        return

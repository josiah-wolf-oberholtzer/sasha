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
                print '{}: Exiting'.format(proc_name)
                self.task_queue.task_done()
                break
            print '\t{}: {} {}'.format(proc_name, task, task.offset)
            task(proc_name=proc_name, **self.kwargs)
            self.result_queue.put(task)
            self.task_queue.task_done()
# -*- coding: utf8 -*-
import logging
import multiprocessing
import threading
import time
import Queue

__author__ = 'augustsun'
log = logging.getLogger(__name__)


class Job(object):
    def __init__(self):
        self.error = None
        self.data = dict()
        self.result = None


class Worker(object):
    def __init__(self, exit_flag, job_queue, done_queue, max_job_num=-1):
        self.exit_flag = exit_flag
        self.job_queue = job_queue
        self.done_queue = done_queue
        self.max_job_num = max_job_num

    def is_alive(self):
        return False

    def do_works(self):
        # log.info('worker work now')
        print 'worker work now'
        #3.只要退出标记没有设定，每个worker最多job没超出限制，循环执行
        num = 0
        while not self.exit_flag.value and (self.max_job_num < 0 or num < self.max_job_num):
            #4.从queue中取出job,queue为空的话继续
            try:
                job = self.job_queue.get(True, 1000)
                print 'job==', job
            except Queue.Empty:
                continue
                #5.job数量+1
            num += 1
            try:
                done_job = self.do_job(job)
                done_job.error = None
                self.done_queue.put_nowait(done_job)
            except Exception as e:
                # log.exception('process job failed, error=[{}]'.format(e))
                print e
                job.error = e
                self.done_queue.put_nowait(job)
        # log.info(
        #     'exit worker, exit_flat=[{}], processed_job_num=[{}]'.format(self.exit_flag.value, num))

    def do_job(self, job):
        raise NotImplementedError


class WorkerManager(object):
    """
    创建并监控worker状态，如果worker死掉，重新启动worker
    """

    def __init__(self, exit_flag, job_queue, done_queue, worker_num,
                 worker_constructor, constructor_args=None, constructor_kwargs=None):
        self.exit_flag = exit_flag
        self.worker_num = worker_num
        self.job_queue = job_queue
        self.done_queue = done_queue
        self.worker_constructor = worker_constructor
        self.constructor_args = constructor_args or []
        self.constructor_kwargs = constructor_kwargs or {}
        self.workers = []

    def new_worker(self):
        raise NotImplementedError

    def monitor_worker(self):
        check_round = 99
        self.workers = []
        while not self.exit_flag.value:
            check_round += 1
            if check_round % 100 == 0:
                check_round = 0
                self.workers = [worker for worker in self.workers if worker.is_alive()]
                while len(self.workers) < self.worker_num:
                    worker = self.new_worker()
                    worker.start()
                    self.workers.append(worker)
                if not self.workers:
                    break
                    # time.sleep(1)
        self.exit_flag.value = 1
        #20.如果是flag改变的退出则等待所有进程执行完
        while self.workers:
            time.sleep(0.1)
            self.workers = [worker for worker in self.workers if worker.is_alive()]


class MultiThreadWorkerManager(WorkerManager):
    def new_worker(self):
        print 'create thread'
        worker = self.worker_constructor(self.exit_flag, self.job_queue, self.done_queue,
                                         *self.constructor_args, **self.constructor_kwargs)
        return threading.Thread(target=worker.do_works)


class MultiProcessWorkerManager(WorkerManager):
    def new_worker(self):
        worker = self.worker_constructor(self.exit_flag, self.job_queue, self.done_queue,
                                         *self.constructor_args, **self.constructor_kwargs)
        p = multiprocessing.Process(target=worker.do_works)
        return p


class MultiProcessMultiThreadWorkerManager(WorkerManager):
    def __init__(self, exit_flag, job_queue, done_queue, process_num, thread_num,
                 worker_constructor, constructor_args=None, constructor_kwargs=None):
        WorkerManager.__init__(self, exit_flag, job_queue, done_queue,
                               process_num, worker_constructor, constructor_args,
                               constructor_kwargs)
        self.thread_num = thread_num

    def new_worker(self):
        def start_thread_manager():
            manager = MultiThreadWorkerManager(self.exit_flag, self.job_queue,
                                               self.done_queue,
                                               self.thread_num, self.worker_constructor,
                                               self.constructor_args, self.constructor_kwargs)
            manager.monitor_worker()

        return multiprocessing.Process(target=start_thread_manager)


# class EchoWorker(Worker):
#     def do_job(self, job):
#         import pprint
#
#         pprint.pprint(job)
#         return job
#
# exit_flag = multiprocessing.Value('i', 0, lock=True)
# worker_num = 2
# job_queue = multiprocessing.Queue(10000)
# done_queue = multiprocessing.Queue(10000)
# job = Job()
# job.hello = 'world'
# job_queue.put_nowait(job)
# multi_process_manager_master = MultiProcessMultiThreadWorkerManager(exit_flag,
#                                                                     job_queue, done_queue,
#                                                                     worker_num, 2,
#                                                                     EchoWorker)
# multi_process_manager_master.monitor_worker()

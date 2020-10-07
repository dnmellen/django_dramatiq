import dramatiq
from dramatiq import group

from django_dramatiq.models import Task
from django_dramatiq.test import DramatiqTestCase


class TestGroupCallbacksMiddleareTestCase(DramatiqTestCase):

    def test_worker_runs_group_callbacks_tasks(self):

        # Given an actor defined in the test method
        @dramatiq.actor(max_retries=0)
        def do_work_parallel():
            pass

        @dramatiq.actor(max_retries=0)
        def do_work_last():
            pass

        # Launch a group with a completion callback
        job = group([
            do_work_parallel.message(),
            do_work_parallel.message(),
            do_work_parallel.message(),
        ])
        job.add_completion_callback(do_work_last.message())
        job.run()

        # And I join on the broker
        self.broker.join(do_work_parallel.queue_name)
        self.worker.join()

        # Then 4 finished Tasks should be stored to the database
        self.assertEqual(Task.tasks.filter(status=Task.STATUS_DONE).count(), 4)


# def test_group_callbacks_works(transactional_db, broker, worker):
#     # Given an actor defined in the test method
#     @dramatiq.actor(max_retries=0)
#     def do_work_parallel():
#         pass

#     @dramatiq.actor(max_retries=0)
#     def do_work_last():
#         pass

#     # Launch a group with a completion callback
#     job = group([
#         do_work_parallel.message(),
#         do_work_parallel.message(),
#         do_work_parallel.message(),
#     ])
#     job.add_completion_callback(do_work_last.message())
#     job.run()

#     # And I join on the broker
#     broker.join(do_work_parallel.queue_name)
#     worker.join()

#     # Then 4 finished Tasks should be stored to the database
#     assertEqual(Task.tasks.filter(status=Task.STATUS_DONE).count(), 4)

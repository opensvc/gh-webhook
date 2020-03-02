from job.factory import JobFactory
from signature import verify

job_factory = JobFactory()


#@verify
def pull_request(body):
    return job_factory.create(context_lib_name='github_pull_request', payload=body).run()


#@verify
def push(body):
    return job_factory.create(context_lib_name='github_push', payload=body).run()

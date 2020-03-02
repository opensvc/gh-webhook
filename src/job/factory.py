import json
import logging
import os

from object_factory import ObjectFactory
from job.job import Job


JOB_CONFIG = os.environ.get('JOB_CONFIG', 'job.json')
logging.info('job config file: JOB_CONFIG=%s', JOB_CONFIG)


class JobFactory:
    creator = ObjectFactory().create

    def create(self, context_lib_name, payload):
        context = self.creator(kind='context', lib_name=context_lib_name, name='Context', payload=payload)
        kwargs = {'context': context}
        logging.info(f'create new job for {context.name}, event {context.event}')
        try:
            with open(JOB_CONFIG) as f:
                kwargs.update(json.load(f)[context.name][context.event])
        except:
            logging.info(f'use default job')
            pass

        job = Job(**kwargs)

        runner = self.creator(kind='runner', lib_name=job.runner_lib, name='Runner')
        job.set_runner(runner)

        payload_provider = self.creator(kind='job_payload', lib_name=job.payload_lib, name='JobPayloadProvider')
        job.set_payload_provider(payload_provider)

        return job

import json
import logging
from abc import abstractmethod

import requests

from runner.runner_abstract import RunnerAbstract


class HttpRunnerAbstract(RunnerAbstract):
    @abstractmethod
    def __init__(self, verb):
        super().__init__()
        self.verb = verb

    def execute(self, job):
        url = job.uri
        payload = job.payload
        verb = self.verb
        logging.info(f'request sending {verb} {url}')
        logging.info(f'request payload {json.dumps(payload, indent=4)}')
        response = getattr(requests, verb)(url,
                                           json=payload,
                                           headers=self.headers(job.credentials),
                                           verify=job.tls)
        self._status = response.status_code
        logging.info(f'response status {self._status}')
        self._data = response.json()

    def headers(self, credentials):
        headers = {
            'Accept': 'application/json',
            'content-type': 'application/json',
        }
        headers.update(credentials)
        return headers

import logging
import json
from dataclasses import dataclass, field

from context.context_abstract import ContextAbstract


@dataclass(order=True)
class Job:
    runner_lib: str = 'null'
    context: ContextAbstract = field(default_factory=ContextAbstract)
    runner = None

    # for http runners
    uri: str = None
    credentials: dict = field(default_factory=dict)
    tls: bool = True
    payload_lib: str = None
    payload_provider = None

    # for release runners
    release_files: list = field(default_factory=list)
    release_base_dir: str = ""

    def execute(self):
        if self.runner is not None:
            self.runner.execute(self)

    @property
    def response(self):
        data, status = self.runner.response
        result_data = dict(data)
        result_data.update({'description': self.context.description})
        logging.info(f'job status: {status}, response: {json.dumps(result_data, indent=2)}')
        return result_data, status

    def set_runner(self, runner):
        self.runner = runner

    def set_payload_provider(self, payload_provider):
        self.payload_provider = payload_provider

    @property
    def payload(self):
        return self.payload_provider(self.context)

    def run(self):
        self.execute()
        return self.response

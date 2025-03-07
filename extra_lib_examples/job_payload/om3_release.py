import yaml

from context.github_pull_request import Context
from job_payload.payload_abstract import PayloadProviderAbstract


class JobPayloadProvider(PayloadProviderAbstract):
    @staticmethod
    def __call__(context: Context):
        job_origin = {
            'release': context.description,
        }

        return {
            "options": {
                "job-origin": yaml.safe_dump(job_origin, sort_keys=False),
                "action": context.action,
                "code-to-test": context.tag_name,
                "release-tag": context.tag_name,
                "release-name": context.release_name,
                "pre-release": context.prerelease,
                "draft": context.draft,
            }
        }

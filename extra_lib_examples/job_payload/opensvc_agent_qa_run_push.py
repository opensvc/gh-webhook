import yaml

from context.github_push import Context
from job_payload.payload_abstract import PayloadProviderAbstract


class JobPayloadProvider(PayloadProviderAbstract):
    @staticmethod
    def __call__(context: Context):
        def first_line(text):
            if not text:
                return ""
            else:
                return text.splitlines()[0]

        job_origin = {
            "push": {
                "ref": context.ref,
                "head_message": first_line(context.head["message"]),
                "sha": context.commit_id,
                "url": context.payload["repository"]["html_url"],
                "pusher": context.pusher,
                "commits": [first_line(commit["message"]) for commit in context.payload["commits"]]
            }
        }
        return {
            "options": {
                "job-origin": yaml.safe_dump(job_origin, sort_keys=False),
                "code-to-test": f"{context.commit_id}"
            }
        }

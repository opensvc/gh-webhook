import yaml

from context.github_pull_request import Context
from job_payload.payload_abstract import PayloadProviderAbstract


class JobPayloadProvider(PayloadProviderAbstract):
    @staticmethod
    def __call__(context: Context):
        desc = context.description
        pr = context.pull_request

        def first_line(text):
            if not text:
                return ""
            else:
                return text.splitlines()[0]

        job_origin = {
            'pull_request': {
                'action': desc["action"],
                'number': desc["pull_request_number"],
                'title': first_line(desc["title"]),
                'login': desc["login"],
                'url': pr["url"],
                'body': first_line(pr["body"]),
                'head': {
                    'ref': pr["head"]["ref"],
                    'sha': pr["head"]["sha"],
                    'url': pr["head"]["repo"]["html_url"]
                },
                'base': {
                    'ref': pr["base"]["ref"],
                    'sha': pr["base"]["sha"],
                    'url': pr["base"]["repo"]["html_url"]
                }
            }
        }
        return {
            "options": {
                "job-origin": yaml.safe_dump(job_origin, sort_keys=False),
                "code-to-test": f"pull/{context.pull_request_number}",
            }
        }

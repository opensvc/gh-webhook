import connexion

from job.factory import JobFactory
from signature import verify

job_factory = JobFactory()


def _event():
    return connexion.request.headers.get('X-GitHub-Event')


def _pong(body):
    return {"message": "pong", "zen": body.get("zen"), "hook_id": body.get("hook_id")}, 200


def _dispatch(context_lib_name, body):
    if _event() == 'ping':
        return _pong(body)
    if 'zen' in body and 'hook_id' in body:
        # ping payload received with a non-ping X-GitHub-Event header
        return {"message": f"ping payload received for X-GitHub-Event: {_event()}"}, 400
    return job_factory.create(context_lib_name=context_lib_name, payload=body).run()


@verify
def pull_request(body):
    return _dispatch('github_pull_request', body)


@verify
def push(body):
    return _dispatch('github_push', body)


@verify
def release(body):
    return _dispatch('github_release', body)

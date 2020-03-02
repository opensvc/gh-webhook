from context.github_abstract import GitHubAbstract


class Context(GitHubAbstract):
    @property
    def event(self):
        return 'push'

    @property
    def head(self):
        return self.payload['head_commit']

    @property
    def ref(self):
        return self.payload['ref']

    @property
    def pusher(self):
        return self.payload['pusher']

    @property
    def commit_id(self):
        return self.head['id']

    @property
    def description(self):
        return {
            'pusher': self.pusher,
            'ref': self.ref,
            'id': self.commit_id,
            'message': self.head['message']
        }
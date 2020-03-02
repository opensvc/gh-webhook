from context.github_abstract import GitHubAbstract


class Context(GitHubAbstract):
    @property
    def event(self):
        return f'pull_request:{self.action}'

    @property
    def pull_request(self):
        return self.payload['pull_request']

    @property
    def pull_request_number(self):
        return self.payload['number']

    @property
    def action(self):
        return self.payload['action']

    @property
    def description(self):
        return {
            'event': 'pull_request',
            'action': self.action,
            'pull_request_number': self.pull_request_number,
            'login': self.pull_request['user']['login'],
            'url': self.url,
            'title': self.pull_request['title'],
            'repository_url': self.url
        }
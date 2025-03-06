from context.github_abstract import GitHubAbstract


class Context(GitHubAbstract):
    """
    Context class for github release events
    """

    @property
    def event(self):
        return f'release:{self.action}'

    @property
    def action(self):
        return self.payload['action']

    @property
    def release(self):
        return self.payload['release']

    @property
    def download_url(self):
        return "%s/releases/download/%s" % (self.html_url, self.tag_name)

    @property
    def release_name(self):
        return self.release['name']

    @property
    def tag_name(self):
        return self.release['tag_name']

    @property
    def draft(self):
        return self.release['draft']

    @property
    def prerelease(self):
        return self.release['prerelease']

    @property
    def login(self):
        return self.release['author']['login']

    @property
    def target_commitish(self):
        return self.release['target_commitish']

    @property
    def repository(self):
        return self.payload['repository']

    @property
    def html_url(self):
        return self.repository['html_url']

    @property
    def description(self):
        return {
            'action': self.action,
            'name': self.name,
            'release_name': self.release_name,
            'tag_name': self.tag_name,
            'draft': self.draft,
            'prerelease': self.prerelease,
            'target_commitish': self.target_commitish,
            'html_url': self.html_url,
            'login': self.login,
        }

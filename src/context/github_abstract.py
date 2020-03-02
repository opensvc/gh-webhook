from dataclasses import dataclass
from context.context_abstract import ContextAbstract


@dataclass(order=True)
class GitHubAbstract(ContextAbstract):
    payload: dict

    @property
    def repository(self):
        return self.payload['repository']

    @property
    def url(self):
        return self.repository['html_url']

    @property
    def name(self):
        return self.url

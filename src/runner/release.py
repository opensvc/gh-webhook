import logging
import os

import requests

from runner.runner_abstract import RunnerAbstract


def download_to(url, dest):
    logging.info("download %s ...", url)
    r = requests.get(url, allow_redirects=True)
    open(dest, 'wb').write(r.content)
    logging.info("installed %s", dest)


class Runner(RunnerAbstract):
    def download_url(self, job, name):
        return "%s/%s" % (job.context.download_url, name)

    def extra_action(self, job):
        """
        extra actions to be run after asset files installed
        return message
        """
        return ""

    def release_dir(self, job):
        """
        default destination dir for release files (<release_base_dir>/<event release tag_name>/)
        """
        return "%s/%s" % (job.release_base_dir, job.context.tag_name)

    def execute(self, job):
        """
        runner example:
         - download assets files from DEPLOY_FILES list
         - install files to release_dir/
        """
        if job.context.action != "published":
            self._data = {
                "message": f'release action {job.context.action} {job.context.name} nothing to do'
            }
            return
        if not job.release_base_dir:
            self._data = {
                "message": f'release action {job.context.action} {job.context.name} skipped (undefined release_base_dir)'
            }
            return
        dest_dir = self.release_dir(job)
        os.makedirs(dest_dir, exist_ok=True)
        deployed_files = set()
        for file in job.release_files:
            dest = f"{dest_dir}/{file}"
            download_to(self.download_url(job, file), dest)
            deployed_files.add(dest)
        extra_action_message = self.extra_action(job)
        message = f'release {job.context.release_name} {job.context.name}, '\
                  f'event: {job.context.event}, '\
                  f'deployed file: {deployed_files}'
        if extra_action_message:
            message = f'{message}, {extra_action_message}'
        self._data = {'message': message}

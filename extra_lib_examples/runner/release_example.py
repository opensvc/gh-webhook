import os

from runner.release import Runner as ReleaseRunner


class Runner(ReleaseRunner):
    def extra_action(self, job):
        """
        update symlink <api_version>/current -> <tag>/bundle
        """
        release_dir = self.release_dir(job)
        version_dir = os.path.dirname(release_dir)
        current = os.path.join(version_dir, "current")
        bundle = os.path.join(os.path.basename(release_dir), 'bundle')
        try:
            os.unlink(current)
        except:
            # ignore broken link
            pass
        os.symlink(bundle, current)
        return f"current {current} is now {bundle}"

    def release_dir(self, job):
        """
        define release dir from event tag name value
        examples:
            v1.9.5 -> <release_base_dir>/1/1.9.5/
            v2.0.0 -> <release_base_dir>/2/2.0.0/
        """
        tag_name = job.context.tag_name.lstrip("v")
        api_version = tag_name.split(".")[0]
        return "%s/%s/%s" % (job.release_base_dir, api_version, tag_name)

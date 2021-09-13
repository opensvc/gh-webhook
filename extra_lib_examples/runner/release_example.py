from runner.release import Runner as ReleaseRunner


class Runner(ReleaseRunner):
    def extra_action(self, job):
        return " current link updated:..."

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

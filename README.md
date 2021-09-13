# webhook job runner (support github webhook)

webhook job processor supporting github webhook for pull request, push, release.

when SECRET env var is defined signature is verified

bundled `runner_lib method: http_post, release`

## how to use

* Prepare your extra lib directory
  
  see bellow for `payload libs` details

        mkdir -p ~/extra_lib/job_payload/
        cp <your python job_payload python files>  ~/extra_lib/job_payload/

  if custom runner

        mkdir -p ~/extra_lib/runner/
        cp <your python runner python files>  ~/extra_lib/runner/
    
* Prepare your job definition file

  see bellow for `jobs config file` details

        mkdir -p ~/.config
        vim ~/.config/job.json

* start webhook listener

        # Default environments settings
        # HOST=127.0.0.1
        # PORT=8080
        # APIS="swagger/github.yaml"
        # BRANCHES="(master)"
        
        # multiple accepted branch example: BRANCHES="(mybranch|master|anotherbranch)"
        
        export EXTRA_LIB=~/extra_lib
        export SECRET=the-secret-defined-on-github-webhook
        export JOB_CONFIG=~/.config/job.json
        python src/kapp.py

## jobs config file (environment variable: JOB_CONFIG)
job config file is a json file, that define keys.

    {
        "<key>": {
            "<event_name>": {
                "runner_lib": "a_runner_lib",
                "uri": "uri used to create job",
                "credentials": {},
                "payload_lib": "a_lib_to_create_job_payload_for_uri"
                "tls": true,
                "release_files": ["asset_file1_to_release", "asset_file2_to_release"],
                "release_base_dir": "base dir path for release"
            }
        } 
    }

    # Needed prop for default 'release' event:
      - release_files
      - release_base_dir

    # Needed prop for 'pull_request:...', 'push' events with 'http_post' runner_lib
      - uri
      - credentials
      - payload_lib
      - tls

## bundled runner libs

### http_post

    create payload from <payload_lib>
    POST <uri> header=<credentials> json=payload verify=<tls>

### release

    When release event action is 'published'
      for each <file> from <release_files>
        download <repository html_url>/<event release tag_name>/<file>
        install downloaded file to <release_base_dir>/<event release tag_name>/

## job config examples
### jobs config file example for github

Here is an example of github webhook listener for repository https://github.com/opensvc/webhook
listening on events:
   * pull request action opened: event is 'pr_opened'
   * push: event is 'push'
                                                               
Pull request open will launch the following job:
* method: http_post
* destination: https://rundeck.domain/api/27/job/job-xxx-pr/run
* credential added to post header: {"X-Rundeck-Auth-Token": "the-job-token"}
* payload for post will be created using lib: job-xxx-pr-opened


    {
      "https://github.com/opensvc/repository": {
        "pull_request:opened": {
          "runner_lib": "http_post",
          "uri": "https://rundeck.domain/api/27/job/job-xxx-pr/run",
          "credentials": {"X-Rundeck-Auth-Token": "the-job-token"},
          "payload_lib": "job-example-pr-opened"
        },
        "push": {
          "runner_lib": "http_post",
          "uri": "https://rundeck.domain/api/27/job/job-xxx-push/run",
          "credentials": {"X-Rundeck-Auth-Token": "the-job-token"},
          "payload_lib": "job-example-pr-push"
        }
        "release": {
          "runner_lib": "release",
          "release_files": ["index.js", "index.html"],
          "release_base_dir": "/deploy_dir"
        }
      },
      "https://github.com/opensvc/other": {
        "release": {
          "runner_lib": "release_custom1",
          "release_files": ["index.js", "index.html"],
          "release_base_dir": "/deploy_dir"
        }
      }
    }

## extra_lib directory

    extra_lib/
             |_ job_payload/
                           |_ job-example-pr-opened.py
                           |_ job-example-push.py
 
             |_ runner/
                           |_ release_custom1.py

## payload libs
### depending on your jobs, you may create a payload lib for each jobs
a job payload lib must define a `class JobPayloadProvider(PayloadProviderAbstract)`

This class must define method: `def __call__(context: Context):` that will provide json parameters for http_post method

* `context` attribute that can be used to create job payload
  context objects are instance of `ContextAbstract` sub classes

### minimum payload lib

    from context.github_push import Context
    from job_payload.payload_abstract import PayloadProviderAbstract
    
    
    class JobPayloadProvider(PayloadProviderAbstract):
        @staticmethod
        def __call__(context: Context):
            return {}
    

### example payload lib `job-example-pr-opened` for a rundeck job that needs `code-to-test` options


    from context.github_push import Context
    from job_payload.payload_abstract import PayloadProviderAbstract
    
    
    class JobPayloadProvider(PayloadProviderAbstract):
        @staticmethod
        def __call__(context: Context):`
            "will create a payload with the context.commit_id value"
            return {
                "options": {
                    "code-to-test": f"{context.commit_id}"
                }
            }

### example custom release lib

    from runner.release_runner import Runner as ReleaseRunner
    
    
    class Runner(ReleaseRunner):
      def extra_action(self, job):
        return "current link updated:..."
      
      def release_dir(self, job):
        tag_name = job.context.tag_name.lstrip("v")
        api_version = tag_name.split(".")[0]
        return "%s/%s/%s" % (job.release_base_dir, api_version, tag_name)

## Example of github event listener for github pull requests

    from job.factory import JobFactory
    from signature import verify
    
    job_factory = JobFactory()
    
    @verify
    def pull_request(body):
        return job_factory.create(context_lib_name='github_pull_request', payload=body).run()
  

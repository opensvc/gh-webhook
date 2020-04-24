# webhook job runner (support github webhook)

webhook job processor supporting github webhook for pull request, push.

bundled `runner_lib method: http_post`

## how to use

* Prepare your extra lib directory
  
  see bellow for `payload libs` details

        mkdir -p ~/extra_lib/job_payload/
        cp <your python job_payload python files>  ~/extra_lib/job_payload/

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
                "tls": true
            }
        } 
    }

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
      "https://github.com/opensvc/webhook": {
        "pr_opened": {
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
    }

## extra_lib directory

    extra_lib/
             |_ job_payload/
                           |_ job-example-pr-opened.py
                           |_ job-example-push.py
 
## payload libs
### depending on your jobs, you may create a payload lib for each jobs
a job payload lib must define a `class JobPayloadProvider(PayloadProviderAbstract)`

This class must define method: `def __call__(context: Context):` that will provide json parameters for http_post method

* `context` attribute that can be used to create job payload
  context objects are instance of `ContextAbstract` sub classes

### minimum lib

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

## Example of github event listener for github pull requests

    from job.factory import JobFactory
    from signature import verify
    
    job_factory = JobFactory()
    
    @verify
    def pull_request(body):
        return job_factory.create(context_lib_name='github_pull_request', payload=body).run()
  

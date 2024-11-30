import pandas as pd

from .client import BATCH_CLIENT


def create_job_queue(name: str, compute_environment: str, tags: dict[str, str] = {}) -> None:
    """Create a new job queue.

    Parameters
    ----------
    name : str
        The name of the job queue.
    compute_environment : str
        The name or ARN of the compute environment to use.
    tags : dict[str, str]
        The tags to apply to the job queue.
    """
    # get the ARN of the compute environment if it is not already an ARN
    if "arn" not in compute_environment:
        compute_environments = BATCH_CLIENT.describe_compute_environments(computeEnvironments=[compute_environment])[
            "computeEnvironments"
        ]
        if len(compute_environments) == 0:
            raise ValueError(f"Compute environment {compute_environment} does not exist.")
        # get the ARN
        compute_environment = compute_environments[0]["computeEnvironmentArn"]

    # create the job queue
    BATCH_CLIENT.create_job_queue(
        jobQueueName=name,
        state="ENABLED",
        priority=1,
        computeEnvironmentOrder=[
            {
                "order": 1,
                "computeEnvironment": compute_environment,
            }
        ],
        tags=tags,
        jobStateTimeLimitActions=[
            {
                "reason": "MISCONFIGURATION:COMPUTE_ENVIRONMENT_MAX_RESOURCE",
                "state": "RUNNABLE",
                "maxTimeSeconds": 600,
                "action": "CANCEL",
            },
            {
                "reason": "MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT",
                "state": "RUNNABLE",
                "maxTimeSeconds": 600,
                "action": "CANCEL",
            },
        ],
    )
    print(f"Job queue {name} created.")


def list_job_queues():
    """List all job queues."""
    table_dict = {
        "Name": [],
        "State": [],
        # "Priority": [],
        "Status": [],
        "Compute Environment": [],
        # "Tags": [],
    }
    job_queues = BATCH_CLIENT.describe_job_queues()
    for job_queue in job_queues["jobQueues"]:
        # check that the non-required fields is in the response
        if "state" not in job_queue:
            continue
        if "priority" not in job_queue:
            continue
        if "status" not in job_queue:
            continue
        if "computeEnvironmentOrder" not in job_queue:
            continue
        if "tags" not in job_queue:
            continue
        table_dict["Name"].append(job_queue["jobQueueName"])
        table_dict["State"].append(job_queue["state"])
        # table_dict["Priority"].append(job_queue["priority"])
        table_dict["Status"].append(job_queue["status"])
        table_dict["Compute Environment"].append(
            job_queue["computeEnvironmentOrder"][0]["computeEnvironment"].split("/")[-1]
        )
        # table_dict["Tags"].append(job_queue["tags"])
    print(pd.DataFrame(table_dict).to_markdown(index=False))


def toggle_job_queue(name: str) -> None:
    """Toggle the state of a job queue.

    Parameters
    ----------
    name : str
        The name or ARN of the job queue.
    """
    job_queues = BATCH_CLIENT.describe_job_queues(jobQueues=[name])["jobQueues"]
    if len(job_queues) == 0:
        raise ValueError(f"Job queue {name} does not exist.")
    job_queue = job_queues[0]
    if job_queue["state"] == "ENABLED":
        BATCH_CLIENT.update_job_queue(jobQueue=name, state="DISABLED")
    else:
        BATCH_CLIENT.update_job_queue(jobQueue=name, state="ENABLED")
    print(f"Job queue {name} is now {job_queue['state']}")


def delete_job_queue(name: str) -> None:
    """Delete a job queue.

    Parameters
    ----------
    name : str
        The name or ARN of the job queue.
    """
    job_queues = BATCH_CLIENT.describe_job_queues(jobQueues=[name])["jobQueues"]
    if len(job_queues) == 0:
        raise ValueError(f"Job queue {name} does not exist.")
    BATCH_CLIENT.delete_job_queue(jobQueue=name)
    print(f"Job queue {name} deleted.")

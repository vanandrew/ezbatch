from typing import Literal

import pandas as pd

from .client import BATCH_CLIENT, IAM_CLIENT
from .conf import CONFIG


def create_compute_environment(
    name: str,
    service_role: str = CONFIG.Settings.serviceRole,
    type: Literal["FARGATE", "EC2"] = "FARGATE",
    max_vcpus: int = CONFIG.Settings.maxvCpus,
    subnets: list[str] = CONFIG.Settings.subnets,
    security_group_ids: list[str] = CONFIG.Settings.securityGroupIds,
    tags: dict[str, str] = {},
):
    """Create a new compute environment.

    Parameters
    ----------
    name : str
        The name of the compute environment.
    service_role : str, optional
        The service role to use for the compute environment. Default is the service role in the configuration
    type : Literal["FARGATE", "EC2"], optional
        The type of compute environment to create. Default is "FARGATE".
    max_vcpus : int, optional
        The maximum number of vCPUs for the compute environment. Default is the maximum vCPUs in the configuration
    subnets : list[str], optional
        The subnets to use for the compute environment. Default is the subnets in the configuration.
    security_group_ids : list[str], optional
        The security group IDs to use for the compute environment. Default is the security group IDs in the configuration.
    tags : dict[str, str]
        The tags to apply to the compute environment.
    """
    # check that the service role exists
    if "Role" not in IAM_CLIENT.get_role(RoleName=service_role.split("/")[-1]):
        raise ValueError(f"Service role {service_role} does not exist.")

    BATCH_CLIENT.create_compute_environment(
        computeEnvironmentName=name,
        type="MANAGED",
        state="ENABLED",
        serviceRole=service_role,
        computeResources={
            "type": type,
            "maxvCpus": max_vcpus,
            "subnets": subnets,
            "securityGroupIds": security_group_ids,
            "tags": tags,
        },
    )


def list_compute_environments():
    """List all compute environments."""
    table_dict = {
        "Name": [],
        # "ARN": [],
        "State": [],
        "Type": [],
        "Max vCPUs": [],
        # "Subnets": [],
        # "Security Group IDs": [],
        # "Tags": [],
    }
    compute_environments = BATCH_CLIENT.describe_compute_environments()
    for compute_environment in compute_environments["computeEnvironments"]:
        # check that the non-required fields is in the response
        if "state" not in compute_environment:
            continue
        if "computeResources" not in compute_environment:
            continue
        if "securityGroupIds" not in compute_environment["computeResources"]:
            continue
        if "tags" not in compute_environment:
            continue
        table_dict["Name"].append(compute_environment["computeEnvironmentName"])
        # table_dict["ARN"].append(compute_environment["computeEnvironmentArn"])
        table_dict["State"].append(compute_environment["state"])
        table_dict["Type"].append(compute_environment["computeResources"]["type"])
        table_dict["Max vCPUs"].append(compute_environment["computeResources"]["maxvCpus"])
        # table_dict["Subnets"].append(compute_environment["computeResources"]["subnets"])
        # table_dict["Security Group IDs"].append(compute_environment["computeResources"]["securityGroupIds"])
        # table_dict["Tags"].append(compute_environment["tags"])
    print(pd.DataFrame(table_dict).to_markdown(index=False))


def toggle_compute_environment(name: str):
    """Toggle the state of a compute environment.

    Parameters
    ----------
    name : str
        The name or ARN of the compute environment to toggle
    """
    # get the current state
    compute_environments = BATCH_CLIENT.describe_compute_environments(computeEnvironments=[name])
    # check if computeEnvironment field is empty
    if not compute_environments["computeEnvironments"]:
        raise ValueError(f"Compute environment {name} does not exist.")
    # check if state in the response
    if "state" not in compute_environments["computeEnvironments"][0]:
        raise ValueError(f"State of compute environment {name} is not available.")
    state = "ENABLED" if compute_environments["computeEnvironments"][0]["state"] == "DISABLED" else "DISABLED"
    BATCH_CLIENT.update_compute_environment(computeEnvironment=name, state=state)
    print(f"Compute environment {name} is now {state}")


def delete_compute_environment(name: str):
    """Delete a compute environment.

    Parameters
    ----------
    name : str
        The name or ARN of the compute environment to delete
    """
    BATCH_CLIENT.delete_compute_environment(computeEnvironment=name)

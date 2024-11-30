from .client import BATCH_CLIENT


def create_compute_environment(name: str, service_role: str | None = None):
    """Create a new compute environment."""
    BATCH_CLIENT.create_compute_environment(
        computeEnvironmentName=name,
        type="MANAGED",
        state="ENABLED",
        serviceRole="",
        tags={},
    )

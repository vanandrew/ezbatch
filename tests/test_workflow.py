from ezbatch.s3 import S3Mount, S3Mounts
from ezbatch.workflow import EZBatchJob, EZBatchWorkflow


def test_workflow():
    """Test the EZBatch workflow."""
    workflow = EZBatchWorkflow(
        name="test-workflow",
        jobs={
            "job1": EZBatchJob(
                image="public.ecr.aws/ubuntu/ubuntu:22.04",
                command="echo hello, world!; ls -l /mnt/CIT168; sleep 18000;",
                environment={"TEST": "test"},
                mounts=S3Mounts(
                    read=[
                        S3Mount(
                            source="s3://research-turing-development-datasets/references/atlas/CIT168",
                            destination="/mnt/CIT168",
                            options="--recursive",
                        ),
                    ],
                    write=[
                        S3Mount(
                            source="/mnt/CIT168",
                            destination="s3://research-turing-scratch/avan/CIT168",
                            options="--recursive --sse aws:kms --sse-kms-key-id mrk-4eeeb45de27844f1bbcc077472b28d97",
                        ),
                    ],
                ),
            ),
        },
    )
    workflow.submit(queue="DefaultFargateQueue")
    workflow.save("tests/test_workflow.json")

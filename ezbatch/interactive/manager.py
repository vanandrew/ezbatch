from typing import cast

from textual import on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Markdown, Select

from ezbatch.job import list_jobs


class EZBatchManager(App):
    """EZBatchManager Application"""

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme = "textual-dark"
        self.jobs = list_jobs("DefaultFargateQueue", "SUCCEEDED")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield VerticalScroll(
            Select(
                options=[(job[1].Name, job[1].JobId) for job in self.jobs.iterrows()],
                prompt="Select a Job to view.",
                id="job-select",
            ),
            Markdown(markdown="# Job Details", id="job-details"),
        )

    @on(Select.Changed, "#job-select")
    def select_changed(self, event: Select.Changed):
        job_id = str(event.value)
        job = self.jobs.loc[self.jobs.JobId == job_id]
        cast(Markdown, self.query_one("#job-details")).update(
            f"# Job Details\n\n{job.to_markdown(index=False)}\n\n" "[Google](https://google.com)"
        )

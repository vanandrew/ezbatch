from pathlib import Path
from typing import cast

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    Footer,
    Header,
    Markdown,
    Select,
    TabbedContent,
    TabPane,
)

from ezbatch.job import list_jobs

THIS_DIR = Path(__file__).resolve().parent


class EZBatchManager(App):
    """EZBatchManager Application"""

    CSS_PATH = str(THIS_DIR / "manager.tcss")
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme = "textual-dark"
        self.job_status = "RUNNING"
        self.jobs = list_jobs("DefaultFargateQueue", self.job_status).to_markdown(index=False)  # type: ignore

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with TabbedContent(id="tabs"):
            with TabPane("Jobs", id="jobs"):
                with Vertical(id="sidebar"):
                    with Center():
                        yield Select(
                            options=[
                                ("SUBMITTED", "SUBMITTED"),
                                ("PENDING", "PENDING"),
                                ("RUNNABLE", "RUNNABLE"),
                                ("STARTING", "STARTING"),
                                ("RUNNING", "RUNNING"),
                                ("SUCCEEDED", "SUCCEEDED"),
                                ("FAILED", "FAILED"),
                            ],
                            allow_blank=False,
                            value="RUNNING",
                            prompt="Job Status",
                            id="job-status-select",
                            classes="sidebar-element",
                        )
                    with Center():
                        yield Button("Refresh", id="refresh-jobs", classes="sidebar-element")
                with VerticalScroll(id="main-content"):
                    yield Markdown(markdown=self.jobs, id="jobs-markdown")
            with TabPane("Queues", id="queues"):
                yield Markdown(markdown="# Queues", id="queues-markdown")
            with TabPane("Compute Environments", id="compute-environments"):
                yield Markdown(markdown="# Compute Environments", id="compute-environments-markdown")

    @on(Button.Pressed, "#refresh-jobs")
    def on_refresh(self, event: Button.Pressed):
        self.jobs = list_jobs("DefaultFargateQueue", self.job_status).to_markdown(index=False)  # type: ignore
        cast(Markdown, self.query_one("#jobs-markdown")).update(self.jobs)

    @on(Select.Changed, "#job-status-select")
    def select_changed(self, event: Select.Changed):
        self.job_status = event.value

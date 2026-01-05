from nomad.actions import TaskQueue
from pydantic import Field
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from nomad.config.models.plugins import ActionEntryPoint


class MyActionEntryPoint(ActionEntryPoint):
    task_queue: str = Field(
        default=TaskQueue.CPU, description='Determines the task queue for this action'
    )

    def load(self):
        from nomad.actions import Action

        from dummy_nomad_plugin.actions.myaction.activities import get_request
        from dummy_nomad_plugin.actions.myaction.workflows import ExampleWorkflow

        return Action(
            task_queue=self.task_queue,
            workflow=ExampleWorkflow,
            activities=[get_request],
        )


my_action = MyActionEntryPoint(
    name='MyAction',
    description='My custom action.',
)

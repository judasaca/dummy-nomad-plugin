from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

from dummy_nomad_plugin.actions.myaction.models import GetRequestInput

with workflow.unsafe.imports_passed_through():
    from dummy_nomad_plugin.actions.myaction.activities import get_request


@workflow.defn
class ExampleWorkflow:
    @workflow.run
    async def run(self, data: GetRequestInput) -> dict:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
        )
        # get_request_input = GetRequestInput(
        #     url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'
        #     f'cid/{data.cid}/property/Title,SMILES/JSON',
        #     timeout=10,
        # )
        result = await workflow.execute_activity(
            get_request,
            data,
            # get_request_input,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        return result

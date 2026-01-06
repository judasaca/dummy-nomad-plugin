from temporalio import activity
from temporalio.workflow import sleep

from dummy_nomad_plugin.actions.myaction.models import GetRequestInput


@activity.defn
async def get_request(data: GetRequestInput):
    for _ in range(data.iterations):
        print('Performing get_request activity...')
        await sleep(10)
    return {'status': 'success', 'data': 'Sample data'}

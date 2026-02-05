import asyncio

from temporalio import activity

from dummy_nomad_plugin.actions.myaction.models import GetRequestInput


@activity.defn
async def get_request(data: GetRequestInput):
    for _ in range(data.iterations):
        activity.logger.info('Waiting 10 seconds...')
        await asyncio.sleep(10)
    return {'status': 'success', 'data': 'Sample data'}

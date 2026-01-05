from temporalio import activity

from dummy_nomad_plugin.actions.myaction.models import GetRequestInput


@activity.defn
async def get_request(data: GetRequestInput):
    """
    Perform a GET request to the specified URL with the provided timeout.
    """
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.get(
            data.url,
            timeout=data.timeout,
        ) as response:
            response.raise_for_status()
            return await response.json()

import asyncio
from loguru import logger
from py_eth_async.data.models import Networks
from py_eth_async.client import Client
from tasks.woofi import WooFi
from private_data import private_key1


async def main():
    client = Client(private_key=private_key1, network=Networks.Arbitrum)
    woofi = WooFi(client=client)
    res = await woofi.swap_usdc_to_eth()
    if res:
        if 'Failed' in res:
            logger.error(res)
        else:
            logger.success(res)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

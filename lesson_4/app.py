import asyncio
from loguru import logger

from py_eth_async.data.models import Networks, TokenAmount
from py_eth_async.client import Client

from data.models import Contracts
from tasks.stargate import Stargate
from tasks.coredao import CoreBridge
from private_data import private_key1
from tasks.woofi import WooFi
from py_eth_async.data.models import Network


async def main():
    client = Client(private_key=private_key1, network=Networks.BSC)
    # print(Networks.Avalanche)
    coredao = CoreBridge(client=client)
    # stargate = Stargate(client=client)
    # await stargate.get_network_with_usdc()
    # print(await Stargate.get_network_with_usdc())
    # await get_network_with_usdc()
    # status = await stargate.send_usdc(
    #     to_network=Networks.BSC,
    #     amount=TokenAmount(2, decimals=6),
    #     dest_fee=TokenAmount(0.014),
    #     max_fee=5
    # )

    status = await coredao.send_usdt_to_core(
        to_network=Networks.CoreDAO,
        amount=TokenAmount(0.2),
    )

    if 'Failed' in status:
        logger.error(status)
    else:
        logger.success(status)

    # status = await stargate.send_usdc_from_avalanche_to_usdt_bsc(
    #     amount=TokenAmount(0.5, decimals=6),
    #     dest_fee=TokenAmount(0.005),
    #     max_fee=1.1
    # )
    # $5.55
    # $0.74

    # 3.27
    # 1.89
    #

    # res = await client.transactions.decode_input_data(
    #     client=client,
    #     contract=Contracts.AVALANCHE_USDC,
    #     input_data='0x9fbf10fc000000000000000000000000000000000000000000000000000000000000006600000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000002b8491765536b7d4fe3e59db46596e1f577ecb000000000000000000000000000000000000000000000000000000000007a120000000000000000000000000000000000000000000000000000000000007975c000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002386f26fc1000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000014002b8491765536b7d4fe3e59db46596e1f577ecb0000000000000000000000000000000000000000000000000000000000000000000000000000000000000014002b8491765536b7d4fe3e59db46596e1f577ecb0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    # )
    # for key, val in res[1].items():
    #     if isinstance(val, bytes):
    #         print(key, val.hex())
    #     elif isinstance(val, tuple):
    #         print(key, '(', end=' ')
    #         for item in val:
    #             if isinstance(item, bytes):
    #                 print(item.hex(), end=', ')
    #             else:
    #                 print(item, end=', ')
    #         print(')')
    #     else:
    #         print(key, val)
    # for key, val in res[1].items():
    #     if isinstance(val, bytes):
    #         print(key, val.hex())
    #
    #     elif isinstance(val, tuple):
    #         print(key, '(', end='')
    #         for item in val:
    #             if isinstance(item, bytes):
    #                 print(item.hex(), end=', ')
    #             else:
    #                 print(item, end=', ')
    #         print(')')
    #     else:
    #         print(key, val)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

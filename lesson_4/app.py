import asyncio
from loguru import logger

from py_eth_async.data.models import Networks, TokenAmount
from py_eth_async.client import Client

from data.models import Contracts
from tasks.stargate import Stargate
from tasks.coredao import CoreBridge
from private_data import private_key1
from tasks.uniswap import Uniswap
from tasks.woofi import WooFi
from py_eth_async.data.models import Network


async def main():
    client = Client(private_key=private_key1, network=Networks.Arbitrum)
    # print(Networks.Avalanche)
    coredao = CoreBridge(client=client)
    uniswap = Uniswap(client=client)
    status = await uniswap.swap(
        amount=TokenAmount(0.001),
        to_token=Contracts.ARBITRUM_GETH
    )
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

    # status = await coredao.send_usdt_to_core(
    #     to_network=Networks.CoreDAO,
    #     amount=TokenAmount(0.2),
    # )
    #
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
    #     contract=Contracts.ARBITRUM_UNISWAP,
    #     input_data='0x000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000038d7ea4c68000000000000000000000000000000000000000000000000000ddbfec7bf8bf198200000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002b82af49447d8a07e3bd95bd0d56f35241523fbab10001f4dd69db25f6d620a7bad3023c5d32761d353d3de9000000000000000000000000000000000000000000',
    #
    # )
    # print(hex(500000000000000))
    # print(res)

    #
    # for val, key in res[1].items():
    #     if val == 'inputs':
    #         for item in key:
    #             print(item.hex())
    # print(hex0x64e616e1'))
    #
    # first = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x8d~\xa4\xc6\x80\x00'
    # second = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x8d~\xa4\xc6\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdd\xbf\xec{\xf8\xbf\x19\x82\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00+\x82\xafID}\x8a\x07\xe3\xbd\x95\xbd\rV\xf3RAR?\xba\xb1\x00\x01\xf4\xddi\xdb%\xf6\xd6 \xa7\xba\xd3\x02<]2v\x1d5==\xe9\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    #
    # print(second.hex())
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

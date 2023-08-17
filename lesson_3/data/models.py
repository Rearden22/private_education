from pretty_utils.type_functions.classes import Singleton
from py_eth_async.data.models import RawContract, DefaultABIs
from pretty_utils.miscellaneous.files import read_json

from data.config import ABIS_DIR


class TokenName(Singleton):
    ETH = 'ETH'
    USDC = 'USDC'
    USDT = 'USDT'
    WBTC = 'WBTC'
    ARB = 'ARB'


class Contracts(Singleton):
    ARBITRUM_WOOFI = RawContract(
        address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30', abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    )

    ARBITRUM_USDC = RawContract(
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831', abi=DefaultABIs.Token
    )

    ARBITRUM_USDT = RawContract(
        address='0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9', abi=DefaultABIs.Token
    )

    ARBITRUM_WBTC = RawContract(
        address='0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f', abi=DefaultABIs.Token
    )

    ARBITRUM_ARB = RawContract(
        address='0x912CE59144191C1204E64559FE8253a0e49E6548', abi=DefaultABIs.Token
    )

    ARBITRUM_ETH = RawContract(
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', abi=DefaultABIs.Token
    )

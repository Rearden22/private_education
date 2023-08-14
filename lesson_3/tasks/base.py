import asyncio
from typing import Optional
import logging
import aiohttp
from py_eth_async.client import Client
from py_eth_async.data.models import TokenAmount
from data.models import TokenName
from data.config import logger


class Base:
    def __init__(self, client: Client):
        self.client = client

    async def get_decimals(self, contract_address: str) -> int:
        contract = await self.client.contracts.default_token(contract_address=contract_address)
        return await contract.functions.decimals().call()

    async def approve_interface(self, token_address: str, spender: str, amount: Optional[TokenAmount] = None) -> bool:
        logger.info(
            f'{self.client.account.address} | start approve token_address: {token_address} for spender: {spender}'
        )
        balance = await self.client.wallet.balance(token=token_address)
        if balance.Wei <= 0:
            logger.error(f'{self.client.account.address} | approve | zero balance')
            return False

        if not amount or amount.Wei > balance.Wei:
            amount = balance

        approved_amount = await self.client.transactions.approved_amount(
            token=token_address,
            spender=spender
        )
        if amount.Wei <= approved_amount.Wei:
            return True
        tx = await self.client.transactions.approve(
            token=token_address,
            spender=spender,
            amount=amount.Wei
        )
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return True
        return False

    async def get_token_price(self, from_token=TokenName.ETH, to_token=TokenName.USDT, default_value=-1) -> float:
        for _ in range(5):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            f'https://min-api.cryptocompare.com/data/price?fsym='
                            f'{from_token.upper()}&tsyms={to_token.upper()}',
                            headers=self.client.headers,
                            proxy=self.client.proxy
                    ) as r:
                        result_dict = await r.json()
                        if 'HasWarning' in result_dict and not result_dict['HasWarning']:
                            return default_value

                        return result_dict[to_token]

            except:
                logging.exception(f'get_eth_price {from_token}')
                await asyncio.sleep(5)

        raise Exception('Failed to get token price!')

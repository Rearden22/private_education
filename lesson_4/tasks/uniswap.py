import time
from py_eth_async.data.models import TxArgs, TokenAmount, RawContract
import json
import aiohttp
from typing import Optional
from web3.types import TxParams
from tasks.base import Base
from data.config import logger
from data.models import Contracts
from web3.contract import AsyncContract


class Uniswap(Base):

    async def get_swap_token_price(
            self,
            amount: TokenAmount,
            to_token: AsyncContract,
            to_token_symbol: str = 'GETH'
    ) -> Optional[TokenAmount]:
        data = {
            "tokenInChainId": self.client.network.chain_id,
            "tokenIn": "ETH",
            "tokenOutChainId": self.client.network.chain_id,
            "tokenOut": to_token.address,
            "amount": str(amount.Wei),
            "type": "EXACT_INPUT",
            "configs": [
                {
                    "protocols": [
                        "V2",
                        "V3",
                        "MIXED"
                    ],
                    "routingType": "CLASSIC"
                }
            ]
        }

        headers = {
            'origin': 'https://app.uniswap.org',
        }

        async with aiohttp.ClientSession() as session:
            logger.info(
                f'{self.client.account.address} | getting {to_token_symbol} price')
            async with session.post('https://api.uniswap.org/v2/quote', headers=headers, data=json.dumps(data)) as r:
                if r.status != 200:
                    logger.error(f"code: {r.status} | can't get price info for swap")
                    return None
                else:
                    data_json = await r.json()
                    return TokenAmount(int(data_json['quote']['route'][0][0]['amountOut']), wei=True)

    async def swap(
            self,
            to_token: RawContract,
            amount: Optional[TokenAmount] = None,
    ):
        to_token_contract = await self.client.contracts.default_token(contract_address=to_token.address)
        to_token_symbol = await to_token_contract.functions.symbol().call()
        failed_text = f'Failed to swap ETH to {to_token_symbol} via Uniswap'
        try:
            uniswap_contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_UNISWAP)
            to_token_price = await self.get_swap_token_price(amount=amount, to_token=to_token_contract,
                                                             to_token_symbol=to_token_symbol)
            if not to_token_price:
                raise ValueError("Can't get destination token price")
            logger.info(f'{self.client.account.address} | Uniswap | swap ETH to {to_token_symbol} | '
                        f'amount: {amount.Ether}')

            args = TxArgs(
                commands='0x0b00',
                inputs=(
                    f'0x{"2".zfill(64)}{hex(amount.Wei)[2:].zfill(64)}',
                    f'0x{"1".zfill(64)}{hex(amount.Wei)[2:].zfill(64)}{hex(to_token_price.Wei)[2:].zfill(64)}'
                    f'{"a0".zfill(64)}'
                    f'{"".zfill(64)}{"2b".zfill(64)}82af49447d8a07e3bd95bd0d56f35241523fbab10001f4dd69db25f6d620a7ba'
                    f'{"d3023c5d32761d353d3de9".ljust(64, "0")}'
                ),
                deadline=int(time.time() + 60 * 5)
            )

            if not amount:
                raise ValueError(f"I haven't amount for swap {self.client.network.name}")

            native_balance = await self.client.wallet.balance()
            if native_balance.Wei < amount.Wei:
                raise ValueError(f'To low native balance: balance: {native_balance.Ether}; value: {amount.Ether}')

            tx_params = TxParams(
                to=uniswap_contract.address,
                data=uniswap_contract.encodeABI('execute', args=args.tuple()),
                value=amount.Wei
            )

            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
            if receipt:
                return f'{amount.Ether} ETH was swapped to {to_token_symbol} via Uniswap: {tx.hash.hex()}'
            return f'{failed_text}!'

        except Exception as e:
            return f'{failed_text}: {e}'

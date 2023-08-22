from py_eth_async.data.models import Network, TxArgs, TokenAmount
import asyncio
import random
from typing import Optional
from web3.types import TxParams
from web3.contract import AsyncContract
from tasks.base import Base
from data.config import logger
from data.models import Contracts


class CoreBridge(Base):
    @staticmethod
    async def get_value(router_contract: AsyncContract) -> Optional[TokenAmount]:
        res = await router_contract.functions.estimateBridgeFee(
            True,
            '0x',
        ).call()
        return TokenAmount(amount=res[0], wei=True)

    async def send_usdt_to_core(
            self,
            to_network: Network,
            amount: Optional[TokenAmount] = None,
    ):
        failed_text = f'Failed to send {self.client.network.name} USDT to {to_network.name} USDT via CoreDao Bridge'
        if self.client.network.name == to_network.name:
            raise AttributeError('The same source network and destination network')
        try:
            usdt_contract = await self.client.contracts.default_token(contract_address=Contracts.BINANCE_USDT)
            coredao_contract = await self.client.contracts.get(contract_address=Contracts.BINANCE_COREDAO_BRIDGE)

            if not amount:
                amount = await self.client.wallet.balance(token=usdt_contract.address)

            logger.info(
                f'{self.client.account.address} | CoreDao Bridge | '
                f'send USDT from {self.client.network.name} to {to_network.name} | amount: {amount.Ether}')

            core_call_params = TxArgs(
                refundAddress=self.client.account.address,
                zroPaymentAddress='0x0000000000000000000000000000000000000000',
            )

            args = TxArgs(
                token=usdt_contract.address,
                amountLD=amount.Wei,
                to=self.client.account.address,
                callParams=core_call_params.tuple(),
                adapterParams='0x'
            )

            value = await self.get_value(router_contract=coredao_contract)
            if not value:
                raise ValueError(f'can not get value {self.client.network.name}')

            native_balance = await self.client.wallet.balance()
            if native_balance.Wei < value.Wei:
                raise ValueError(f'To low native balance: balance: {native_balance.Ether}; value: {value.Ether}')

            if await self.approve_interface(
                    token_address=usdt_contract.address,
                    spender=coredao_contract.address,
                    amount=amount
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                raise ValueError('| can not approve')

            tx_params = TxParams(
                to=coredao_contract.address,
                data=coredao_contract.encodeABI('bridge', args=args.tuple()),
                value=value.Wei
            )

            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
            if receipt:
                return (f'{amount.Ether} USDT was send from {self.client.network.name} to {to_network.name} '
                        f'via CoreDao Bridge: {tx.hash.hex()}')
            return f'{failed_text}!'

        except Exception as e:
            return f'{failed_text}: {e}'

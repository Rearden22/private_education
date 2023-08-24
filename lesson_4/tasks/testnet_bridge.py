from py_eth_async.data.models import TxArgs, TokenAmount
import asyncio
import random
from typing import Optional
from web3.types import TxParams
from web3.contract import AsyncContract
from tasks.base import Base
from data.config import logger
from data.models import Contracts


class TestnetBridge(Base):
    async def get_value(self, router_contract: AsyncContract, amount: TokenAmount) -> Optional[TokenAmount]:
        res = await router_contract.functions.estimateSendFee(
            154,
            self.client.account.address,
            amount.Wei,
            False,
            '0x'
        ).call()
        return TokenAmount(amount=int(res[0]), wei=True)

    async def get_params(
            self,
            amount: TokenAmount,
            testnet_bridge_contract: AsyncContract,
    ) -> tuple[TxArgs, Optional[TokenAmount]]:

        args = TxArgs(
            _from=self.client.account.address,
            _dstChainId=154,
            _toAddress=self.client.account.address,
            _amount=amount.Wei,
            _refundAddress=self.client.account.address,
            _zroPaymentAddress='0x0000000000000000000000000000000000000000',
            _adapterParams=b''
        )

        value = await self.get_value(
            router_contract=testnet_bridge_contract,
            amount=amount
        )

        return args, value

    async def send_geth_to_goerli(
            self,
            amount: Optional[TokenAmount] = None,
    ):
        failed_text = f'Failed to send {self.client.network.name} GETH to Goerli GETH via Testnet Bridge'
        try:
            geth_contract = await self.client.contracts.default_token(contract_address=Contracts.ARBITRUM_GETH)
            testnet_bridge_contract = await (self.client.contracts.get
                                             (contract_address=Contracts.ARBITRUM_TESTNET_BRIDGE))

            if not amount:
                amount = await self.client.wallet.balance(token=geth_contract.address)

            logger.info(
                f'{self.client.account.address} | TestnetBridge | '
                f'send GETH from {self.client.network.name} to Goerli | amount: {amount.Ether}')

            args, value = await self.get_params(
                amount=amount,
                testnet_bridge_contract=testnet_bridge_contract
            )

            if not value:
                raise ValueError(f'can not get value {self.client.network.name}')

            native_balance = await self.client.wallet.balance()
            if native_balance.Wei < value.Wei:
                raise ValueError(f'To low native balance: balance: {native_balance.Ether}; value: {value.Ether}')

            if await self.approve_interface(
                    token_address=geth_contract.address,
                    spender=testnet_bridge_contract.address,
                    amount=amount
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                raise ValueError('| can not approve')

            tx_params = TxParams(
                to=testnet_bridge_contract.address,
                data=testnet_bridge_contract.encodeABI('sendFrom', args=args.tuple()),
                value=value.Wei  # В транзах велью в 3 раза больше, чем даёт смарт контракт, но уходит и без умножения
            )

            tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
            receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
            if receipt:
                return (f'{amount.Ether} GETH was send from {self.client.network.name} to Goerli '
                        f'via TestnetBridge: {tx.hash.hex()}')
            return f'{failed_text}!'

        except Exception as e:
            return f'{failed_text}: {e}'

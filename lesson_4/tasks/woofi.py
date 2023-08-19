import asyncio
from typing import Optional
from web3.types import TxParams
from py_eth_async.data.models import TxArgs, TokenAmount
from py_eth_async.data.models import RawContract

from data.models import Contracts
from tasks.base import Base


class WooFi(Base):
    async def swap(
            self,
            to_token: RawContract,
            from_token: RawContract,
            amount: Optional[TokenAmount] = None,
            slippage: float = 1
    ):
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)

        from_token_name = 'ETH'
        to_token_name = 'ETH'
        if from_token.address != Contracts.ARBITRUM_ETH.address:
            from_token_contract = await self.client.contracts.default_token(contract_address=from_token)
            from_token_name = await from_token_contract.functions.symbol().call()
        if to_token != Contracts.ARBITRUM_ETH.address:
            to_token_contract = await self.client.contracts.default_token(contract_address=to_token)
            to_token_name = await to_token_contract.functions.symbol().call()

        if from_token.address == Contracts.ARBITRUM_ETH.address:
            from_token_balance = await self.client.wallet.balance()
        else:
            from_token_balance = await self.client.wallet.balance(token=from_token.address)

        if not amount:
            if from_token.address == Contracts.ARBITRUM_ETH.address:
                amount = TokenAmount(amount=float(from_token_balance.Ether) * 0.5)
            else:
                amount = from_token_balance

        failed_text = f'Failed swap {from_token_name} {amount.Ether} to {to_token_name} via WooFi'

        if amount.Wei > from_token_balance.Wei:
            return f'{failed_text}: To low balance: {from_token_balance.Ether}'

        from_token_price = await self.get_token_price(token=from_token_name)
        to_token_price = await self.get_token_price(token=to_token_name)

        min_to_amount = TokenAmount(
            amount=from_token_price / to_token_price * float(amount.Ether) * (1 - slippage / 100),
            decimals=await self.get_decimals(contract_address=to_token.address)
        )

        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
            value=amount.Wei if from_token.address == Contracts.ARBITRUM_ETH.address else 0
        )

        if from_token.address != Contracts.ARBITRUM_ETH.address:
            await self.approve_interface(token_address=from_token.address, spender=contract.address, amount=amount)
            await asyncio.sleep(5)

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swaped to {min_to_amount.Ether} {to_token_name} via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'

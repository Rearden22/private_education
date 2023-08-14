import asyncio
from typing import Optional
from web3.types import TxParams
from py_eth_async.data.models import TxArgs, TokenAmount
from data.models import Contracts, NetworkName, TokenName
from tasks.base import Base


class WooFi(Base):
    async def swap(
            self,
            from_token: TokenName,  # Не уверен, что здесь надо приводить к типу TokenName
            to_token: TokenName,  # Не уверен, что здесь надо приводить к типу TokenName
            amount: Optional[TokenAmount] = None,
            network: NetworkName = NetworkName.ARBITRUM,  # Не уверен, что здесь надо приводить к типу NetworkName
            slippage: float = 1
    ):

        failed_text = f'Failed swap {from_token} to {to_token} via WooFi'
        contract = await self.client.contracts.get(contract_address=getattr(Contracts, f'{network}_WOOFI'))

        from_token_contract = getattr(Contracts, f'{network}_{from_token}')
        to_token_contract = getattr(Contracts, f'{network}_{to_token}')

        token_price = await self.get_token_price(from_token=from_token, to_token=to_token)

        if from_token == TokenName.ETH:
            min_to_amount = TokenAmount(
                amount=token_price * float(amount.Ether) * (1 - slippage / 100),
                decimals=await self.get_decimals(contract_address=to_token_contract.address)
            )
        else:
            if not amount:
                amount = await self.client.wallet.balance(token=from_token_contract)

            await self.approve_interface(
                token_address=from_token_contract.address,
                spender=contract.address,
                amount=amount
            )
            await asyncio.sleep(5)

            if to_token is not TokenName.ETH:
                min_to_amount = TokenAmount(
                    amount=float(amount.Ether) * token_price * (1 - slippage / 100), # здесь после token_price поменял / на *
                    decimals=await self.get_decimals(contract_address=to_token_contract.address)
                )
            else:
                min_to_amount = TokenAmount(
                    amount=float(amount.Ether) * token_price * (1 - slippage / 100), # здесь после token_price поменял / на *
                )

        args = TxArgs(
            fromToken=from_token_contract.address,
            toToken=to_token_contract.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
        )

        if from_token == TokenName.ETH:
            tx_params['value'] = amount.Wei

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return (f'{amount.Ether} {from_token} was swaped to '
                    f'{min_to_amount.Ether} {to_token} via WooFi: {tx.hash.hex()}')

        return f'{failed_text}!'

    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.ETH,
            to_token=TokenName.USDC,
            amount=amount,
            network=network,
            slippage=slippage
        )

    async def swap_usdc_to_eth(
            self,
            amount: Optional[TokenAmount] = None,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.USDC,
            to_token=TokenName.ETH,
            amount=amount,
            network=network,
            slippage=slippage
        )

    async def swap_eth_to_usdt(
            self,
            amount: TokenAmount,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.ETH,
            to_token=TokenName.USDT,
            amount=amount,
            network=network,
            slippage=slippage
        )

    async def swap_usdt_to_eth(
            self,
            amount: Optional[TokenAmount] = None,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.USDT,
            to_token=TokenName.ETH,
            amount=amount,
            network=network,
            slippage=slippage
        )

    async def swap_eth_to_wbtc(
            self,
            amount: TokenAmount,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.ETH,
            to_token=TokenName.WBTC,
            amount=amount,
            network=network,
            slippage=slippage
        )

    async def swap_wbtc_to_eth(
            self,
            amount: Optional[TokenAmount] = None,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.WBTC,
            to_token=TokenName.ETH,
            amount=amount,
            network=network,
            slippage=slippage
        )

    async def swap_eth_to_arb(
            self,
            amount: TokenAmount,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.ETH,
            to_token=TokenName.ARB,
            amount=amount,
            network=network,
            slippage=slippage
        )

    async def swap_arb_to_usdc(
            self,
            amount: Optional[TokenAmount] = None,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.ARB,
            to_token=TokenName.USDC,
            amount=amount,
            network=network,
            slippage=slippage
        )

    async def swap_usdc_to_arb(
            self,
            amount: Optional[TokenAmount] = None,
            network: NetworkName = NetworkName.ARBITRUM,
            slippage: float = 1
    ):
        await self.swap(
            from_token=TokenName.USDC,
            to_token=TokenName.ARB,
            amount=amount,
            network=network,
            slippage=slippage
        )

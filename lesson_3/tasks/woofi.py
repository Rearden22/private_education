import asyncio
from typing import Optional
from web3.types import TxParams
from py_eth_async.data.models import TxArgs, TokenAmount
from data.models import Contracts, TokenName
from tasks.base import Base
from loguru import logger


class WooFi(Base):
    async def swap(
            self,
            from_token_ticker: str,
            to_token_ticker: str,
            from_token_contract: Contracts.ARBITRUM_ETH,
            to_token_contract: Contracts.ARBITRUM_USDC,
            amount: Optional[TokenAmount] = None,
            slippage: float = 1
    ):
        failed_text = f'Failed swap {from_token_ticker} to {to_token_ticker} via WooFi'
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)
        token_price = await self.get_token_price(from_token=from_token_ticker, to_token=to_token_ticker)
        if token_price == -1:
            logger.error("Can't get a token price. The program will be closed")
            exit()

        if from_token_ticker == TokenName.ETH:
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

            if to_token_ticker is not TokenName.ETH:
                min_to_amount = TokenAmount(
                    amount=float(amount.Ether) * token_price * (1 - slippage / 100),
                    decimals=await self.get_decimals(contract_address=to_token_contract.address)
                )
            else:
                min_to_amount = TokenAmount(
                    amount=float(amount.Ether) * token_price * (1 - slippage / 100),
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

        if from_token_ticker == TokenName.ETH:
            tx_params['value'] = amount.Wei

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return (f'{amount.Ether} {from_token_ticker} was swaped to '
                    f'{min_to_amount.Ether} {to_token_ticker} via WooFi: {tx.hash.hex()}')

        return f'{failed_text}!'

    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.ETH,
            to_token_ticker=TokenName.USDC,
            from_token_contract=Contracts.ARBITRUM_ETH,
            to_token_contract=Contracts.ARBITRUM_USDC,
            amount=amount,
            slippage=slippage
        )

    async def swap_usdc_to_eth(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.USDC,
            to_token_ticker=TokenName.ETH,
            from_token_contract=Contracts.ARBITRUM_USDC,
            to_token_contract=Contracts.ARBITRUM_ETH,
            amount=amount,
            slippage=slippage
        )

    async def swap_eth_to_usdt(
            self,
            amount: TokenAmount,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.ETH,
            to_token_ticker=TokenName.USDT,
            from_token_contract=Contracts.ARBITRUM_ETH,
            to_token_contract=Contracts.ARBITRUM_USDT,
            amount=amount,
            slippage=slippage
        )

    async def swap_usdt_to_eth(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.USDT,
            to_token_ticker=TokenName.ETH,
            from_token_contract=Contracts.ARBITRUM_USDT,
            to_token_contract=Contracts.ARBITRUM_ETH,
            amount=amount,
            slippage=slippage
        )

    async def swap_eth_to_wbtc(
            self,
            amount: TokenAmount,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.ETH,
            to_token_ticker=TokenName.WBTC,
            from_token_contract=Contracts.ARBITRUM_ETH,
            to_token_contract=Contracts.ARBITRUM_WBTC,
            amount=amount,
            slippage=slippage
        )

    async def swap_wbtc_to_eth(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.WBTC,
            to_token_ticker=TokenName.ETH,
            from_token_contract=Contracts.ARBITRUM_WBTC,
            to_token_contract=Contracts.ARBITRUM_ETH,
            amount=amount,
            slippage=slippage
        )

    async def swap_eth_to_arb(
            self,
            amount: TokenAmount,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.ETH,
            to_token_ticker=TokenName.ARB,
            from_token_contract=Contracts.ARBITRUM_ETH,
            to_token_contract=Contracts.ARBITRUM_ARB,
            amount=amount,
            slippage=slippage
        )

    async def swap_arb_to_usdc(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.ARB,
            to_token_ticker=TokenName.USDC,
            from_token_contract=Contracts.ARBITRUM_ARB,
            to_token_contract=Contracts.ARBITRUM_USDC,
            amount=amount,
            slippage=slippage
        )

    async def swap_usdc_to_arb(
            self,
            amount: Optional[TokenAmount] = None,
            slippage: float = 1
    ):
        await self.swap(
            from_token_ticker=TokenName.USDC,
            to_token_ticker=TokenName.ARB,
            from_token_contract=Contracts.ARBITRUM_USDC,
            to_token_contract=Contracts.ARBITRUM_ARB,
            amount=amount,
            slippage=slippage
        )

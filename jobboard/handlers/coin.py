from web3 import Web3, HTTPProvider
import json

from web3.middleware import geth_poa_middleware
from web3.utils.validation import validate_address
from django.conf import settings


class CoinHandler(object):
    def __init__(self, contract_address=None, account=None):
        self.web3 = Web3(HTTPProvider(settings.NODE_URL))
        self.web3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.contract_address = contract_address or settings.VERA_COIN_CONTRACT_ADDRESS
        self.account = account or settings.WEB_ETH_COINBASE
        with open('jobboard/handlers/coin_abi.json', 'r') as ad:
            self.abi = json.load(ad)
        self.contract = self.web3.eth.contract(abi=self.abi, address=self.contract_address)

    def owner(self):
        return self.contract.call().owner()

    def balanceOf(self, address):
        validate_address(address)
        return self.contract.call().balanceOf(address)

    @property
    def symbol(self):
        return self.contract.call().symbol()

    @property
    def decimals(self):
        return self.contract.call().decimals()

    def totalSupply(self):
        return self.contract.call().totalSupply()

    def allowance(self, owner, spender):
        validate_address(owner)
        validate_address(spender)
        return self.contract.call().allowance(owner, spender)

    def transfer(self, address, amount):
        validate_address(address)
        return self.contract.transact({'from': settings.WEB_ETH_COINBASE}).transfer(address, amount)

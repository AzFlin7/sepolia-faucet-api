from web3 import Web3
from eth_account import Account
from bip39 import mnemonic_to_seed

def get_account_from_mnemonic(mnemonic):
    seed = mnemonic_to_seed(mnemonic)
    account = Account.from_mnemonic(mnemonic)
    return account
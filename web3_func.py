from web3 import Web3
from web3 import Account

# 将私钥转换为地址
def key_to_address(private_key):
    w3 = Web3()
    account = Account.from_key(private_key)
    address = account.address
    return address


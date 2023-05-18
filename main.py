from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from web3_func import key_to_address
from time import sleep
import random

def mint_bear(private_key):
    account_from = {
        'private_key': private_key,
        'address': key_to_address(private_key),
    }
    print(f'start mint address:{account_from["address"]}')
    # 连接到Polygon Mumbai测试网
    w3 = Web3(Web3.HTTPProvider('https://rpc-mainnet.matic.quiknode.pro'))

    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # 部署的合约地址
    contract_address = '0x8E0DCCa4E6587d2028ed948b7285791269059a62' 

    with open('rbear_abi.json', 'r') as f:
        # 从abi_usdc.json文件中读取abi
        rbear_abi = json.load(f)

    # 连接到合约接口
    contract = w3.eth.contract(address=contract_address, abi=rbear_abi)  

    balance = w3.eth.get_balance(account_from['address'])
    print("账户余额: ", balance)

    # 构造claim方法参数
    _receiver = account_from['address']
    _quantity = 1
    _currency = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    _pricePerToken = 0
    _allowlistProof_proof = '0x0000000000000000000000000000000000000000000000000000000000000000'
    _allowlistProof_proof = w3.to_bytes(hexstr=_allowlistProof_proof)
    _allowlistProof_quantityLimitPerWallet = 1
    _allowlistProof_pricePerToken = 0
    _allowlistProof_currency = _currency 
    _data = b'0x'

    # 调用claim方法,发起交易 
    claim_tx_hash = contract.functions.claim(
                        _receiver, 
                        _quantity,        # uint256
                        _currency,
                        _pricePerToken,   # uint256
                        ([_allowlistProof_proof],
                        _allowlistProof_quantityLimitPerWallet,   # uint256
                        _allowlistProof_pricePerToken,            # uint256 
                        _allowlistProof_currency),
                        _data
                    ).build_transaction(
        {
            'from': account_from['address'],
            'nonce': w3.eth.get_transaction_count(account_from['address']),
            'value': 0,
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,   
        }
    )

    tx_create = w3.eth.account.sign_transaction(claim_tx_hash, account_from['private_key'])

    tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)

    # 等待交易确认 
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash


def main():
    with open('keys.txt', 'r') as f:
        keys = f.read()
        key_list = keys.split('\n')

    key_num = len(key_list)
    for idx, private_key in enumerate(key_list):
        print(f'No.{idx+1} / {key_num}')
        tx_hash = mint_bear(private_key)
        print(f"Transaction: https://polygonscan.com/tx/{tx_hash.hex()}")
        sleep(random.randint(5, 10))

main()
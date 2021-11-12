import json
import requests
import pandas as pd

from web3 import Web3 

# https://etherscan.io/tx/0x31d079ce35bf43328b40fb679a7628e8f323861a08aba1a1eb1827fac570edc0

start_block_number = 13425115

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/af1d3ad9016c423282f5875d6e2dc6a7"))
print(w3.isConnected())

target_topics = [
    "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822", # swap
    "0x4c209b5fc8ad50758f13e2e1088ba56a560dff690a1c6fef26394f4c03821c4f", # mint
    "0xdccd412f0b1252819cb1fd330b93224ca42612892bb3f4f789976e6d81936496", # burn
]

txn_list = {}

for block_number in range(start_block_number - 1, start_block_number + 50):
    if block_number not in txn_list:
        txn_list[block_number] = []
    block = json.loads(Web3.toJSON(w3.eth.get_block(block_number, False)))
    for transaction in block['transactions'][:2]:
        txn_receipt = json.loads(Web3.toJSON(w3.eth.get_transaction_receipt(transaction)))
        if txn_receipt['to'] == '0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f': # sushiswap
            continue

        logs = txn_receipt['logs']
        for log in logs:
            if log['topics'][0] in target_topics:
                txn_list[block_number].append(transaction)
                break

print(txn_list)

# curl -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0xccd9db", true],"id":1}' localhost:8545
# curl -X POST 


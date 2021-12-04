from abc import abstractstaticmethod
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()


install_solc('0.8.7')

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Compile solidity files

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version='0.8.7',
)
# print(compiled_sol)


# Saved compiled code to json file
with open('compiled_code.json', "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]
# print(abi)


# connect to ganache
w3 = Web3(Web3.HTTPProvider(os.getenv('W3_ADDRESS')))
chain_id = 1337
my_address = os.getenv("ACC_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# build, sign, and send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract, you need:
# Contract ABI
# Contract Address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# We can interact with a contract via:
# - Calls (not interacting with blockchain)
# - Transact (making a state change)
# print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(15).call()) # as it's call, it's not gonna store the value

# Initial value of favourite number
# nonce = w3.eth.getTransactionCount(my_address) + 1
# print(f'nonce: {nonce}')
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {'chainId': chain_id, 'from': my_address, 'nonce': nonce + 1, 'gasPrice': w3.eth.gas_price}
)
signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")

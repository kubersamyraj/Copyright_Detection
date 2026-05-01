from web3 import Web3
import json
import os

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
contract_path = os.path.join(BASE_DIR, "build", "contracts", "CopyrightRegistry.json")

with open(contract_path) as f:
    contract_json = json.load(f)

abi = contract_json["abi"]

contract_address = "0x9571b5cf2b741837E840Fc28EAe7BcbbA7348Db0"

contract = w3.eth.contract(address=contract_address, abi=abi)

account = w3.eth.accounts[0]
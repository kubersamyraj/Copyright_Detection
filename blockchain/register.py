from blockchain.connect import contract, w3, account

def register_hash(hash_value):
    tx = contract.functions.registerWork(hash_value).transact({
        "from": account
    })

    receipt = w3.eth.wait_for_transaction_receipt(tx)

    print("Registered on blockchain")
    print("Transaction:", receipt.transactionHash.hex())
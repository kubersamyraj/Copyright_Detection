from blockchain.connect import contract

def verify_hash(hash_value):
    try:
        owner, timestamp = contract.functions.verifyWork(hash_value).call()

        print("Found on blockchain")
        print("Owner:", owner)
        print("Timestamp:", timestamp)

        return True
    
    except:
        print("Not found on blockchain")
        return False
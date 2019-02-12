#creating the blockchain

import datetime
import hashlib as hashing
import json
from flask import Flask, jsonify


class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash
                 }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
        
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False: 
            #hashing.sha256(String)
            hash_operation = hashing.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof+=1
                
        return new_proof
    
    def hash(self, block):
        #json.dump coverts dictionary to string
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashing.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof =previous_block['proof']
            proof = block['proof']
            hash_operation = hashing.sha256(str(proof**3 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

#Creating the app
app = Flask(__name__)

#creating an instance
blockchain = Blockchain()

@app.route('/mining', methods = ['GET'])
def mining():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    data ={ 'message' : 'CONGRATULATIONS',
           'index' : block['index'],
           'proof' : block['proof'],
           'timestamp' : block['timestamp'],
           'previous_hash' : block['previous_hash']
            }
    return jsonify(data), 200

@app.route('/getChain', methods = ['GET'])
def getChain():
    response = {    'chain' :   blockchain.chain,
                    'length':   len(blockchain.chain)
            }
    return jsonify(response),200


app.run( host = '0.0.0.0', port = 5000)
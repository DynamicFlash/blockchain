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
                 'timestap': str(datetime.datetime.now()),
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
            hash_operation = hashing.sha256(str(new_proof**3 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] is "0000":
                check_proof = True
            else:
                new_proof+=1
                
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sorted_keys = True).encode()
        return hashing.sha256(encoded_block).hexdigest()
    
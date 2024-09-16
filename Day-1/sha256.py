'''
Day-1: 
Learnt about hashing and the difference between Encryption/Decryption and hashing.
Short program to create a SHA-256 hash of the data using the hashlib library in python.
'''

import hashlib

def hash_data(data):
    # Encode the data to bytes, as required by hashlib 
    data_bytes = data.encode('utf-8')
    
    # Create a SHA-256 hash of the data
    sha256_hash = hashlib.sha256(data_bytes).hexdigest()
    
    return sha256_hash

# Takes input from user and hashes it.
data = input("Enter string to Hash.\n")
hashed_data = hash_data(data)
print(f"Original Data: {data}")
print(f"Hashed Data: {hashed_data}")

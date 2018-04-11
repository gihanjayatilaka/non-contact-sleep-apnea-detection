import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5

# Use a larger key length in practice...
KEY_LENGTH = 1024  # Key size (in bits)
random_gen = Random.new().read

# Generate RSA private/public key pairs for both parties...
keypair_snowden = RSA.generate(KEY_LENGTH, random_gen)
keypair_pytn = RSA.generate(KEY_LENGTH, random_gen)

# Public key export for exchange between parties...
pubkey_snowden = keypair_snowden.publickey()
pubkey_pytn = keypair_pytn.publickey()

# Plain text messages...
message_to_snowden = 'You are a patriot!'
message_to_pytn = "Russia is really nice this time of year...\nUse encryption and make the NSA CPUs churn and burn!"

# Generate digital signatures using private keys...
hash_of_snowden_message = MD5.new(message_to_snowden).digest()
signature_pytn = keypair_pytn.sign(hash_of_snowden_message, '')
hash_of_pytn_message = MD5.new(message_to_pytn).digest()
signature_snowden = keypair_snowden.sign(hash_of_pytn_message, '')

# Encrypt messages using the other party's public key...
encrypted_for_snowden = pubkey_snowden.encrypt(message_to_snowden, 32)  # from PyTN
encrypted_for_pytn = pubkey_pytn.encrypt(message_to_pytn, 32)  # from Snowden

# Decrypt messages using own private keys...
decrypted_snowden = keypair_snowden.decrypt(encrypted_for_snowden)
decrypted_pytn = keypair_pytn.decrypt(encrypted_for_pytn)

# Signature validation and console output...
hash_snowden_decrypted = MD5.new(decrypted_snowden).digest()
if pubkey_pytn.verify(hash_snowden_decrypted, signature_pytn):
    print("Edward Snowden received from PyTn:")
    print(decrypted_snowden)
    print("")

hash_pytn_decrypted = MD5.new(decrypted_pytn).digest()
if pubkey_snowden.verify(hash_pytn_decrypted, signature_snowden):
    print("PyTN received from Edward Snowden:")
    print(decrypted_pytn)
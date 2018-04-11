# Inspired from http://coding4streetcred.com/blog/post/Asymmetric-Encryption-Revisited-(in-PyCrypto)
# PyCrypto docs available at https://www.dlitz.net/software/pycrypto/api/2.6/

import Cryptodome
from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import base64

def generate_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 256*4 # use larger value in production
	privatekey = RSA.generate(modulus_length, Random.new().read)
	publickey = privatekey.publickey()
	return privatekey, publickey

def encrypt_message(a_message , publickey):
	encryptor = PKCS1_OAEP.new(publickey)
	encrypted_msg = encryptor.encrypt(a_message)
	#encrypted_msg = encryptor.encrypt(a_message, 32)[0]
	encoded_encrypted_msg = base64.b64encode(encrypted_msg) # base64 encoded strings are database friendly
	return encoded_encrypted_msg

def decrypt_message(encoded_encrypted_msg, privatekey):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decryptor = PKCS1_OAEP.new(privatekey)
	decoded_decrypted_msg =  decryptor.decrypt(decoded_encrypted_msg)
	# decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg

########## BEGIN ##########

a_message = "The quick brown fox jumped over the lazy dog"
privatekey , publickey = generate_keys()
encrypted_msg = encrypt_message(a_message , publickey)
decrypted_msg = decrypt_message(encrypted_msg, privatekey)

print ("%s - (%d)" % (privatekey.exportKey() , len(privatekey.exportKey())))
print ("%s - (%d)" % (publickey.exportKey() , len(publickey.exportKey())))
print (" Original content: %s - (%d)" % (a_message, len(a_message)))
print ("Encrypted message: %s - (%d)" % (encrypted_msg, len(encrypted_msg)))
print ("Decrypted message: %s - (%d)" % (decrypted_msg, len(decrypted_msg)))



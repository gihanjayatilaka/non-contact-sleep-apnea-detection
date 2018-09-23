from Cryptodome.PublicKey import RSA

secret_code = "Unguessable"
key = RSA.generate(2048)

'''Private key'''
print(key.export_key())

encrypted_key = key.export_key(passphrase=secret_code, pkcs=8,
                              protection="scryptAndAES128-CBC")

'''Encrypted private key'''
print(encrypted_key)

file_out = open("rsa_key.bin", "wb")
file_out.write(encrypted_key)

print(key.publickey().export_key())
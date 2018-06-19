import configparser

config = configparser.ConfigParser()

print(config.sections())

config.read('example.ini')

print(config.sections())  # dictionary of dictionary

print(config['bitbucket.org']['User'])
print(config['DEFAULT']['Compression'])

topsecret = config['topsecret.server.com']
print(topsecret['ForwardX11'])

for key in config['bitbucket.org']: print(key)
import json
import random

len = 100
rand_min = 0
rand_max = 200

time = [t for t in range(len)]
val = [random.randint(rand_min, rand_max) for i in range(len)]

dict = {"time" : time, "val" : val}

encoded_data = json.dumps(dict)

print(encoded_data)
print(type(encoded_data))

decoded_data = json.loads(encoded_data)

print(decoded_data)
print(type(decoded_data))
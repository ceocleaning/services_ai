import random

def generate_id(prefix):
    id = ''.join(random.choices('0123456789', k=6))
    print(prefix + id)
    return prefix + id

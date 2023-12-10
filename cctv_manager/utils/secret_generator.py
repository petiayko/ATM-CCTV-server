import random
import string

secret_key_symbols = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('~', '').replace('\'', '').replace('"', '')

secret_key = ''.join([random.choice(secret_key_symbols) for _ in range(50)])

with open('/data/config/cctv_manager/secret_key', 'w+') as secret_file:
    secret_file.write(secret_key)


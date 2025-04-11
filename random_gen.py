#!/usr/bin/env python3

import random
import string

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + "!?"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password

if __name__ == "__main__":
    print(generate_password())

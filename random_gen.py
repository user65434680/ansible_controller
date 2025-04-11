#!/usr/bin/env python3

import random
import string

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + "!?"
    return ''.join(random(characters) for _ in range(length))

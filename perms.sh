#!/bin/bash

find . -type f -name "*.py" -exec chmod 755 {} \;

rm -- "$0"

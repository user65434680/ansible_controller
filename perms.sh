#!/bin/bash

find . -type f -name "*.py" -exec chmod 755 {} \;
find . -type f -name "*.sh" -exec chmod 755 {} \;

rm -- "$0"

#!/bin/bash

set -e

echo "--------------------"
echo "Static type checking"
echo "--------------------"
mypy .

echo "---------------------------------"
echo "Unit testing + coverage gathering"
echo "---------------------------------"

coverage run -m pytest .

echo "------------------------"
echo "Coverage report building"
echo "------------------------"
coverage html -i

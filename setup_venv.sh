#!/bin/bash

set -e

echo "----------------------------"
echo "Building virtual environment"
echo "----------------------------"
# NOTE: VIRTUAL_ENV environment variable is also used by venv.
# So when the venv is deactivated, VIRTUAL_ENV would be empty (and not hold the value set here)
export VIRTUAL_ENV=".venv"

python3 -m venv ${VIRTUAL_ENV}
source ${VIRTUAL_ENV}/bin/activate

pip install pip --upgrade

# Install package in editable mode
# With optional dependencies: to run CI testing
pip install -e .[tests]

if [[ "$SKIP_GITHOOKS" != "true" ]]; then
    echo "-------------------"
    echo "Enable the githooks"
    echo "-------------------"
    pre-commit install
fi

echo "---------"
echo "All done!"
echo "---------"

echo "Please now run 'source ${VIRTUAL_ENV}/bin/activate' to use!"

deactivate

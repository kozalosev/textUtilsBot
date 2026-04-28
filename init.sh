#!/bin/sh

echo "Generating a virtual environment..."
python3 -m venv venv
. venv/bin/activate
echo "Installing dependencies..."
echo
pip install setuptools wheel --upgrade
pip install -r requirements.txt
echo

echo "Creating environment file..."
cp .env.example .env
echo

echo "Done. Edit '.env' with your actual values before running the bot."
echo "Use the '. venv/bin/activate' command to enable the virtual environment. Inside, type 'deactivate' to disable it."
echo "The 'start.sh' script is a shortcut to enter the virtual environment and run the bot."
echo
echo "If you want to run tests, execute the following command in addition:"
echo "    . venv/bin/activate && pip install -r requirements-dev.txt && deactivate"
echo

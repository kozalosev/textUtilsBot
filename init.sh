#!/bin/sh

echo "Generating a virtual environment..."
python3 -m venv venv
. venv/bin/activate
echo "Installing dependencies..."
echo
pip install setuptools wheel --upgrade
pip install -r requirements.txt
echo

echo "Creating a configuration file..."
cp examples/config.py app/
sudo chgrp www-data app/config.py || echo "Group 'www-data' not found. Change the group of 'app/config' file manually!"
chmod o-r app/config.py
echo

echo "Done. Don't forget to replace fake values in 'app/config.py' with your actual ones."
echo "Use the '. venv/bin/activate' command to enable the virtual environment. Inside, type 'deactivate' to disable it."
echo "The 'start.sh' script is a shortcut to enter the virtual environment and run the bot."
echo
echo "If you want to run tests, execute the following command in addition:"
echo "    . venv/bin/activate && pip install -r requirements-dev.txt && deactivate"
echo

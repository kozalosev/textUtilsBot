#!/bin/sh

if [ ! -f "app/data/config.py" ]; then
    echo "A configuration file was not found. Copying the skeleton..."

    cp examples/config.py app/data/config.py
    sudo chgrp www-data app/data/config.py
    chmod o-r app/data/config.py

    echo "Edit the 'app/data/config.py' file and run this script again."
    exit
fi

if cmp --silent "examples/config.py" "app/data/config.py"; then
    echo "Don't forget to change the values in the 'app/data/config.py' file!"
    exit
fi

if [ ! -f "app/data/currates_conf.py" ]; then
    echo "A configuration file was not found. Copying the skeleton..."

    cp examples/currates_conf.py app/data/currates_conf.py
    sudo chgrp www-data app/data/currates_conf.py
    chmod o-r app/data/currates_conf.py

    echo "Edit the 'app/data/currates_conf.py' file and run this script again."
    exit
fi

if cmp --silent "examples/currates_conf.py" "app/data/currates_conf.py"; then
    echo "Don't forget to change the values in the 'app/data/currates_conf.py' file!"
    exit
fi

if [ "$(stat -c "%U" app/data)" != "www-data" ]; then
    echo "The 'app/data' directory must be owned by the 'www-data' user! Trying to fix it..."
    sudo chown www-data app/data
fi

docker-compose up -d --build

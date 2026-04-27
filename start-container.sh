#!/bin/sh

if [ ! -f ".env" ]; then
    echo "No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "Edit '.env' with your actual values and run this script again."
    exit
fi

if cmp --silent ".env.example" ".env"; then
    echo "Don't forget to set real values in '.env'!"
    exit
fi

docker compose up -d --build

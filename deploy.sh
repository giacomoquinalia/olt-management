#!/usr/bin/env bash


if [ "x$1" == "x" ]; then
    echo -e "0 - Production\n1 - Development"
elif [ "$1" == "0" ]; then
    export DJANGO_SETTINGS_MODULE=config.settings.production
    echo "Production settings: $DJANGO_SETTINGS_MODULE"
elif [ "$1" == "1" ]; then
    export DJANGO_SETTINGS_MODULE=config.settings.development
    echo "Development settings: $DJANGO_SETTINGS_MODULE"
else
    echo "Invalid argument."
fi

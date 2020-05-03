#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: bash ./connect_container.sh [container_name]"
    exit
fi

docker attach $(docker ps | grep $1 | cut -d " " -f1)

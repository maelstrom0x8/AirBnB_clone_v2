#!/usr/bin/env bash


if [ "$1" = "test" ]; then
  source ./envars.sh test
  docker-compose down
  docker-compose up -d mysql_test
else
    source ./envars.sh dev
    docker-compose down
    docker-compose up -d mysql_dev
fi

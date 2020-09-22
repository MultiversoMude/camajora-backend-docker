#!/bin/sh

if [ -z "$1" ]
then 
  TAG="11.0"
else
  TAG=$1
fi 

echo "Building $TAG"

docker build --no-cache -t metadonors/camajora-odoo:$TAG .
docker push metadonors/camajora-odoo:$TAG 

#!/bin/bash

BACKUP_PATH=`pwd`
cd `dirname $0`
cd ../

python -m unittest discover

cd $BACKUP_PATH

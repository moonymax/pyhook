#!/bin/bash

if [[ ! -d plugins ]]
then
    mkdir plugins
fi
mv pyhook*.jar plugins/
if [[ ! -d venv ]]
then
    python3 -m venv venv
fi
source venv/bin/activate
pip install py4j==0.10.9.7
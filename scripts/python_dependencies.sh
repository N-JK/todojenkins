#!/usr/bin/env bash

sudo chown -R ubuntu:ubuntu ~/Todo-App
virtualenv /home/ubuntu/Todo-App/venv
source /home/ubuntu/Todo-App/venv/bin/activate
pip install -r /home/ubuntu/Todo-App/requirements.txt
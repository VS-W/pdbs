#!/bin/bash
pip install -r requirements.txt --upgrade --disable-pip-version-check | grep -v -E 'already satisfied|normal site-packages is not writeable'
python3 -m bot.py

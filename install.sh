#!/bin/bash

rm -r /usr/src/keysnek
mkdir -p /usr/src/keysnek
python -m venv /usr/src/keysnek/.venv
/usr/src/keysnek/.venv/bin/pip install evdev
cp ./src /usr/src/keysnek -r
cp ./scripts /usr/src/keysnek -r
cp main.py /usr/src/keysnek
cp keysnek.service /usr/src/keysnek

#!/usr/bin/env bash

cd ~/Library/Application\ Support/xbar/plugins && \
    curl https://raw.githubusercontent.com/LVCarnevalli/poke/main/poke.5m.py -O -J -L -s --output poke.5m.py && \
    echo "OK"
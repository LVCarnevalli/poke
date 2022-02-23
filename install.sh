#!/usr/bin/env bash

cd /tmp && \
    rm -rf poke-main && \
    rm -f poke-main.zip && \
    curl https://github.com/LVCarnevalli/poke/archive/refs/heads/main.zip -O -J -L -s --output poke-main.zip && \
    unzip poke-main.zip -d . && \
    cd poke-main && \
    pip3 install -r requirements.txt && \
    mkdir -p $HOME/poke && \
    cp -rf poke.sh $HOME/poke && \
    cp -rf poke.py $HOME/poke

echo "OK"
echo -e '\n'
echo "Manual steps:"
echo "- export POKE_URL=\"https://server\""
echo "- export PATH=\"\$HOME/poke:\$PATH\""
echo -e '\n'
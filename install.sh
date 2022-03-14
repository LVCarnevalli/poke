#!/usr/bin/env bash

cd /tmp && \
    rm -rf poke-main && \
    rm -f poke-main.zip && \
    curl https://github.com/LVCarnevalli/poke/archive/refs/heads/main.zip -O -J -L -s --output poke-main.zip && \
    unzip poke-main.zip -d . && \
    cd poke-main && \
    pip3 install -r requirements.txt && \
    mkdir -p $HOME/poke && \
    cp -rf poke.py $HOME/poke && \
    cp -rf poke.sh $HOME/poke/poke && \
    chmod 755 $HOME/poke/poke && \
    chmod +x $HOME/poke/poke

if [ "$(uname)" == "Darwin" ]; then
    PYTHON3=$(which python3)
    cat github.poke.plist | \
        sed -e "s|{HOME}|$HOME|g" | \
        sed -e "s|{PYTHON3}|$PYTHON3|g" \
        > ~/Library/LaunchAgents/github.poke.plist && \
        launchctl unload ~/Library/LaunchAgents/github.poke.plist && \
        launchctl load -w ~/Library/LaunchAgents/github.poke.plist
fi

echo "OK"
echo -e '\n'
echo "Manual steps:"
echo "- export PATH=\"\$HOME/poke:\$PATH\""
echo -e '\n'
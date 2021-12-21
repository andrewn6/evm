#!/bin/bash -e

# install the deps required
if [ $(which apt-get) ]; then
  echo "installing deps for mac"
  brew install coreutils make gcc zlib git curl python3 python-dev

else
  echo "** Sorry! this installer is for Mac/Linux with Homebrew installed, you
  can build it with python yourself."
fi

unamestr=$(uname)
if [[ "$unamestr" == 'Linux' ]]; then
  DIR=$(dirname $(readlink -f $0))
elif [[ "$unamestr" == "Darwin" ]]; then
  cmd=$(which "$0")
  if [ -L "$cmd" ]; then
    cmd=$(readlink "$cmd")
  fi
  DIR=$(dirname "$cmd")
else
  echo "Darwin/Linux are only supported!"
  exit
fi

unset PYTHONPATH
echo "***********************"
echo " Thanks for installing my disassembler."
echo " Checkout out readme for info on how to get started"
echo "    ~acn"
exec /usr/bin/env python $DIR/evm/evm.py



#!/bin/bash -e

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
exec /usr/bin/env python $DIR/evm/disassembler.py
echo "*************"
echo " Thanks for installing my disassembler."
echo " Checkout out readme for info"
echo "    ~acn"


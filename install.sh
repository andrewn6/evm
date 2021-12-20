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
echo "***********************"
echo " Thanks for installing my disassembler."
echo " Checkout out readme for info"
echo "You can get started by going to localhost:3000, or you can also use my IDA
plugin.."
echo "    ~acn"
exec /usr/bin/env python $DIR/evm/disassembler.py



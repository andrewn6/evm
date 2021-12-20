# EVM

[![Build Status](https://travis-ci.org/anddddrew/evm.svg?branch-master)](https://travis-ci.org/anddddrew/evm)


## Features
* Disassemble with bytecode
* IDA Plugin (view ida/)
* Recursive decent algorithim for disassembly.
* Docker support

<pre>
Mac/Linux supported out of the box.

Docker image should work everywhere..
</pre>

## Installing

Clone the repo
```git clone https://github.com/anddddrew/evm.git```

Run the installer
```./install```

After this you should have a prompt, and you can start using the disassembler :).

*NOTE: all disassembly output from the script will be in a file called "output"*

## Releases
* 1.2 -- Ida plugin done, bug fixes coming on the way. Added better error handling, small bug fix in the main program.
* 1.1 -- Progress on IDA plugin, dumped hashes. Can disassemble from hex's now
* 1.0 -- Main disassembler working, very basic. Able to disassemble from bytecode only

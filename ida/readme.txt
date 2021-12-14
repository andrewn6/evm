IDA plugin for the evm disassembler.

Simply run ./build.

**directorys**

python/ All code related to the plugin. (using ida python sdk)
- hashes.py all hashes
  - loader.py Script that sets the plugin up, other configuration.
  - cpu.py, main code by manticore (I did not write/claim to write this part over here, I used
    another ida plugin for a similar EVM project)

FROM ubuntu:latest

LABEL maintainer="andrewnijmeh1@gmail.com"
LABEL description="EVM disassembly via bytecode in Python"

WORKDIR /evm

COPY . .

RUN apt-get update && apt-get install -y python3-pip nodejs npm


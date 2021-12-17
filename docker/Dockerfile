FROM ubuntu:18.04

LABEL maintainer="andrewnijmeh1@gmail.com"
LABEL description="Disassembling the EVM."

COPY . /evm
WORKDIR /evm

RUN apt-get upgrade
RUN apt-get update && apt-get -y install gcc g++ git curl python-dev python-virtualenv  
# Make sure to install pip3
RUN apt-get -y install python3-pip

RUN virtualenv venv
RUN bash -c "source venv/bin/activate && pip3 install --upgrade pip"

COPY ../requirements.txt ../requirements.txt
RUN bash -c "source venv/bin/activate && pip3 install --upgrade -r requirements.txt"

RUN ln -sf /evm/evm /usr/local/bin/evm

COPY . .

RUN ./run_tests.sh

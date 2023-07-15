FROM python:3.10

WORKDIR /workdir

COPY requirements.txt /workdir/requirements.txt
COPY requirements-dev.txt /workdir/requirements-dev.txt

RUN python3.10 -m pip install -r requirements-dev.txt
RUN python3.10 -m pip install  -r requirements.txt

RUN make clean-data
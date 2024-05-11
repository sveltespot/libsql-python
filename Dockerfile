FROM rust:slim-bullseye as builder

RUN apt update && apt install -y \
    build-essential git python3-dev python3-pip python3-venv \
    && mkdir /pylibsql /pyenv \
    && python3 -m venv /pyenv \
    && . /pyenv/bin/activate \
    && pip install maturin patchelf pytest

COPY src/ /pylibsql/src/.
COPY tests/ /pylibsql/tests/.
COPY pyproject.toml /pylibsql/.
COPY Cargo.toml /pylibsql/.
COPY Cargo.lock /pylibsql/.

WORKDIR /pylibsql

RUN . /pyenv/bin/activate \
    && maturin develop --release \
    && pytest

FROM debian:bullseye-slim as runtime

RUN apt update && apt install -y \
    python3 python3-venv

COPY --from=builder /pyenv /pyenv
COPY tests/ /pylibsql/tests/.
WORKDIR /pylibsql

ENV PATH="/pyenv/bin:${PATH}"


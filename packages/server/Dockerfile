FROM rust:1.64

RUN rustup default nightly

WORKDIR /usr/src/server

COPY Cargo.toml .
COPY . .

RUN cargo build

CMD ["cargo", "run"]

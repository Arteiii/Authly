FROM rust:latest AS builder

WORKDIR /authly

COPY . .

RUN cargo build --bin authly --release

RUN rm -rf target/release/build \
    && rm -rf target/release/deps \
    && rm -rf target/release/incremental \
    && rm -rf target/release/.fingerprint


FROM debian:latest as runner

RUN apt-get update \
    && apt-get install -y openssl ca-certificates

COPY --from=builder /authly/target/release/authly /usr/local/bin/authly

EXPOSE 8000

CMD ["authly"]

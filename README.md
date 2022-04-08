# elm-package-benchmark

This repository contains a benchmark example using the [elm package universe](https://package.elm-lang.org/). It compares different implementations of package resolver algorithms:
1. PubGrub Rust: [pubgrub-rs](https://github.com/pubgrub-rs/pubgrub)
2. PubGrub in Python: [mixology](https://github.com/sdispater/mixology)

The benchmark resolves the dependencies of every version of every package in the elm package registry.

## Setup Python

Make sure Python 3.9 and Pipenv is installed. Create virtual environment:

    pipenv sync

## Cleanup repository

Delete temporary files:

    bash clean.sh

## Run PubGrub Rust benchmark

Install Rust and clone repository:

    git clone https://github.com/mpizenberg/elm-solve-deps.git

Copy example code:

    ln -s "$PWD/test.rs" elm-solve-deps/elm-solve-deps-lib/examples/test.rs
    cd elm-solve-deps/elm-solve-deps-lib

Compile and run:

    cd elm-solve-deps/elm-solve-deps-lib
    time cargo run --example test > ../../result.yaml
    cd -

## Compare results

Create file `result_rust.json` from `result.yaml`:

    pipenv run python compare.py

Check differences:

    diff result.json result_rust.json


# elm-package-benchmark

Benchmark different dependency resolver implementations using elm package universe.

## Introduction

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

## Download elm package registry

Download all elm package metadata files into the folder `registry`:

    pipenv run python download.py

This also saves the file `graph.json` which contains the whole dependency graph of all package versions. For missing packages it will be automatically assumed that they have only one version and no dependencies, so ignore the message about failed packages.

## Run PubGrub Python benchmark

First check the simple examples:

    pipenv run python example_simple.py
    pipenv run python example.py

They should output the found solution.

Now run the benchmark (takes about 45 seconds):

    pipenv run python example_full.py

This puts the result in `result.json` and prints how many package versions failed to resolve.

## Run PubGrub Rust benchmark

Install Rust and clone repository:

    git clone https://github.com/mpizenberg/elm-solve-deps.git

Copy example code:

    ln -s "$PWD/test.rs" elm-solve-deps/elm-solve-deps-lib/examples/test.rs
    cd elm-solve-deps/elm-solve-deps-lib

Compile:

    cargo build --release --example test

Run benchmark and write result to file (takes about 4 seconds):

    cargo run --release --example test > ../../result.yaml
    cd -

## Compare results

Create file `result_rust.json` from `result.yaml`:

    pipenv run python compare.py

Check differences:

    diff result.json result_rust.json


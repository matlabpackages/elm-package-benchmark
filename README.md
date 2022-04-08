## Run Rust example

Install Rust and clone repository:

    git clone https://github.com/mpizenberg/elm-solve-deps.git

Copy example code:

    ln -s "$PWD/test.rs" elm-solve-deps/elm-solve-deps-lib/examples/test.rs
    cd elm-solve-deps/elm-solve-deps-lib

Compile and run:

    cd elm-solve-deps/elm-solve-deps-lib
    time cargo run --example test > ../../result.yaml
    cd -

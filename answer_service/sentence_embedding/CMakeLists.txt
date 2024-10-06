cmake_minimum_required(VERSION 3.4...3.18)
project(sentence_embedding)
set(CMAKE_PREFIX_PATH "/usr/local/lib/python3.11/site-packages/pybind11")

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(pybind11 REQUIRED)

pybind11_add_module(sentence_embedding
    bindings.cpp
    sentence_embedding.cpp
)

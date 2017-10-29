cmake_minimum_required(VERSION 3.8)
project(code)

set(CMAKE_CXX_STANDARD 11)
include_directories(/usr/lib/llvm-3.8/lib/)
include_directories(/usr/lib/llvm-3.8/include/)
set(SOURCE_FILES main.cpp clang.cpp)
add_executable(code ${SOURCE_FILES})
target_link_libraries(code -lclang)
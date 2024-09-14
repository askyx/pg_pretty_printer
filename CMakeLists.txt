
cmake_minimum_required(VERSION 3.10.0)
project(pg_pretty_printer VERSION 1.0.0)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

find_package(PostgreSQL REQUIRED)
find_package(Python3 REQUIRED)

set(PTINTER ${CMAKE_SOURCE_DIR}/postgres-gdb.py)
set(GDBINIT $ENV{HOME}/.gdbinit)

MESSAGE(STATUS "install printer to postgres path: ${PostgreSQL_BIN_DIR}")
install(FILES ${PTINTER} DESTINATION ${PostgreSQL_BIN_DIR})
install(DIRECTORY ${CMAKE_SOURCE_DIR}/printer DESTINATION ${PostgreSQL_BIN_DIR})

MESSAGE(STATUS "append debugger init file to: ${GDBINIT}")
file(APPEND ${GDBINIT} "add-auto-load-safe-path ${PostgreSQL_BIN_DIR}\n")
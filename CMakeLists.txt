cmake_minimum_required(VERSION 3.16)
project(poly_equation_solver VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(poly_solver
    src/equations.cpp
)

target_include_directories(poly_solver
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
)

add_executable(eqsolver
    src/main.cpp
)

target_link_libraries(eqsolver PRIVATE poly_solver)

include(CTest)
if(BUILD_TESTING)
    add_executable(test_equations
        tests/cpp/test_equations.cpp
    )
    target_link_libraries(test_equations PRIVATE poly_solver)
    add_test(NAME equation_solver_cpp_tests COMMAND test_equations)
endif()

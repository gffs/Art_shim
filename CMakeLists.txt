cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(ArtShim)

list(APPEND CMAKE_PREFIX_PATH $ENV{ROOTSYS})

find_package(ROOT REQUIRED)
include(${ROOT_USE_FILE})

#EXECUTE_PROCESS( COMMAND uname -s COMMAND tr -d '\n' OUTPUT_VARIABLE UNAME_S )
#add_definitions(DEBUG)

set(CMAKE_CXX11_STANDARD_COMPILE_OPTION)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -arch x86_64 -std=c++14 -pipe -Wextra -Wno-shadow -g -O3")

include_directories (
    ${ROOT_INCLUDE_DIRS},
    /usr/local/include
)

ROOT_GENERATE_DICTIONARY(G__ArtShim include/art_shim.h LINKDEF LinkDef.h)
add_library(ArtShim SHARED G__ArtShim.cxx)
target_link_libraries(ArtShim ${ROOT_LIBRARIES})

install(TARGETS ArtShim DESTINATION lib)
install(FILES ${CMAKE_BINARY_DIR}/libArtShim.rootmap DESTINATION lib COMPONENT libraries)
install(FILES ${CMAKE_BINARY_DIR}/libArtShim_rdict.pcm DESTINATION lib COMPONENT libraries)

install(DIRECTORY include/ DESTINATION include FILES_MATCHING PATTERN "*.h")
install(DIRECTORY art_shim/ DESTINATION art_shim FILES_MATCHING PATTERN "*.py")
install(FILES plot_test.py DESTINATION ./)

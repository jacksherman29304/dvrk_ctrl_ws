# cmake_minimum_required(VERSION 3.8)
# project(peg_sim)

# if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
#   add_compile_options(-Wall -Wextra -Wpedantic)
# endif()

# # find dependencies
# find_package(ament_cmake REQUIRED)
# # uncomment the following section in order to fill in
# # further dependencies manually.
# # find_package(<dependency> REQUIRED)

# if(BUILD_TESTING)
#   find_package(ament_lint_auto REQUIRED)
#   # the following line skips the linter which checks for copyrights
#   # comment the line when a copyright and license is added to all source files
#   set(ament_cmake_copyright_FOUND TRUE)
#   # the following line skips cpplint (only works in a git repo)
#   # comment the line when this package is in a git repo and when
#   # a copyright and license is added to all source files
#   set(ament_cmake_cpplint_FOUND TRUE)
#   ament_lint_auto_find_test_dependencies()
# endif()

# ament_package()

cmake_minimum_required(VERSION 3.8)
project(peg_sim)

find_package(ament_cmake REQUIRED)

# ${PROJECT_NAME} expands to peg_sim. 
# DESTINATION is relative to the install prefix, so this lands at install/peg_sim/share/peg_sim/.

install(DIRECTORY ADF ambf_shaders
        DESTINATION share/${PROJECT_NAME})

install(FILES launch.yaml
        DESTINATION share/${PROJECT_NAME})

ament_package()
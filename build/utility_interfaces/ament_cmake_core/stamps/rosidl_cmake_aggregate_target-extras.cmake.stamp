# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target utility_interfaces::utility_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${utility_interfaces_TARGETS}.
if(utility_interfaces_TARGETS AND NOT TARGET utility_interfaces::utility_interfaces)
  add_library(utility_interfaces::utility_interfaces INTERFACE IMPORTED)
  set_target_properties(utility_interfaces::utility_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${utility_interfaces_TARGETS}")
endif()

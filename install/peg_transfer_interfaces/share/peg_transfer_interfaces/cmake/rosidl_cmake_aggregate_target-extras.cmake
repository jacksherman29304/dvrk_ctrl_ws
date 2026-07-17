# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target peg_transfer_interfaces::peg_transfer_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${peg_transfer_interfaces_TARGETS}.
if(peg_transfer_interfaces_TARGETS AND NOT TARGET peg_transfer_interfaces::peg_transfer_interfaces)
  add_library(peg_transfer_interfaces::peg_transfer_interfaces INTERFACE IMPORTED)
  set_target_properties(peg_transfer_interfaces::peg_transfer_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${peg_transfer_interfaces_TARGETS}")
endif()

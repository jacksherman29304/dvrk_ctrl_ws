// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from peg_transfer_interfaces:srv/GetObjectPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "peg_transfer_interfaces/srv/get_object_pose.h"


#ifndef PEG_TRANSFER_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__STRUCT_H_
#define PEG_TRANSFER_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'object_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetObjectPose in the package peg_transfer_interfaces.
typedef struct peg_transfer_interfaces__srv__GetObjectPose_Request
{
  rosidl_runtime_c__String object_name;
} peg_transfer_interfaces__srv__GetObjectPose_Request;

// Struct for a sequence of peg_transfer_interfaces__srv__GetObjectPose_Request.
typedef struct peg_transfer_interfaces__srv__GetObjectPose_Request__Sequence
{
  peg_transfer_interfaces__srv__GetObjectPose_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} peg_transfer_interfaces__srv__GetObjectPose_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in srv/GetObjectPose in the package peg_transfer_interfaces.
typedef struct peg_transfer_interfaces__srv__GetObjectPose_Response
{
  geometry_msgs__msg__Pose pose;
  bool success;
} peg_transfer_interfaces__srv__GetObjectPose_Response;

// Struct for a sequence of peg_transfer_interfaces__srv__GetObjectPose_Response.
typedef struct peg_transfer_interfaces__srv__GetObjectPose_Response__Sequence
{
  peg_transfer_interfaces__srv__GetObjectPose_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} peg_transfer_interfaces__srv__GetObjectPose_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  peg_transfer_interfaces__srv__GetObjectPose_Event__request__MAX_SIZE = 1
};
// response
enum
{
  peg_transfer_interfaces__srv__GetObjectPose_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/GetObjectPose in the package peg_transfer_interfaces.
typedef struct peg_transfer_interfaces__srv__GetObjectPose_Event
{
  service_msgs__msg__ServiceEventInfo info;
  peg_transfer_interfaces__srv__GetObjectPose_Request__Sequence request;
  peg_transfer_interfaces__srv__GetObjectPose_Response__Sequence response;
} peg_transfer_interfaces__srv__GetObjectPose_Event;

// Struct for a sequence of peg_transfer_interfaces__srv__GetObjectPose_Event.
typedef struct peg_transfer_interfaces__srv__GetObjectPose_Event__Sequence
{
  peg_transfer_interfaces__srv__GetObjectPose_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} peg_transfer_interfaces__srv__GetObjectPose_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PEG_TRANSFER_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__STRUCT_H_

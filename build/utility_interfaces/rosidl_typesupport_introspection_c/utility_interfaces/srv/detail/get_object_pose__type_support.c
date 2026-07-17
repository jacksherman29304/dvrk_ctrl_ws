// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from utility_interfaces:srv/GetObjectPose.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "utility_interfaces/srv/detail/get_object_pose__rosidl_typesupport_introspection_c.h"
#include "utility_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "utility_interfaces/srv/detail/get_object_pose__functions.h"
#include "utility_interfaces/srv/detail/get_object_pose__struct.h"


// Include directives for member types
// Member `object_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  utility_interfaces__srv__GetObjectPose_Request__init(message_memory);
}

void utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_fini_function(void * message_memory)
{
  utility_interfaces__srv__GetObjectPose_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_member_array[1] = {
  {
    "object_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(utility_interfaces__srv__GetObjectPose_Request, object_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_members = {
  "utility_interfaces__srv",  // message namespace
  "GetObjectPose_Request",  // message name
  1,  // number of fields
  sizeof(utility_interfaces__srv__GetObjectPose_Request),
  false,  // has_any_key_member_
  utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_member_array,  // message members
  utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_type_support_handle = {
  0,
  &utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_members,
  get_message_typesupport_handle_function,
  &utility_interfaces__srv__GetObjectPose_Request__get_type_hash,
  &utility_interfaces__srv__GetObjectPose_Request__get_type_description,
  &utility_interfaces__srv__GetObjectPose_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_utility_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Request)() {
  if (!utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_type_support_handle.typesupport_identifier) {
    utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__rosidl_typesupport_introspection_c.h"
// already included above
// #include "utility_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__functions.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__struct.h"


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/pose.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  utility_interfaces__srv__GetObjectPose_Response__init(message_memory);
}

void utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_fini_function(void * message_memory)
{
  utility_interfaces__srv__GetObjectPose_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_member_array[2] = {
  {
    "pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(utility_interfaces__srv__GetObjectPose_Response, pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(utility_interfaces__srv__GetObjectPose_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_members = {
  "utility_interfaces__srv",  // message namespace
  "GetObjectPose_Response",  // message name
  2,  // number of fields
  sizeof(utility_interfaces__srv__GetObjectPose_Response),
  false,  // has_any_key_member_
  utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_member_array,  // message members
  utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_type_support_handle = {
  0,
  &utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_members,
  get_message_typesupport_handle_function,
  &utility_interfaces__srv__GetObjectPose_Response__get_type_hash,
  &utility_interfaces__srv__GetObjectPose_Response__get_type_description,
  &utility_interfaces__srv__GetObjectPose_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_utility_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Response)() {
  utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  if (!utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_type_support_handle.typesupport_identifier) {
    utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__rosidl_typesupport_introspection_c.h"
// already included above
// #include "utility_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__functions.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "utility_interfaces/srv/get_object_pose.h"
// Member `request`
// Member `response`
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  utility_interfaces__srv__GetObjectPose_Event__init(message_memory);
}

void utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_fini_function(void * message_memory)
{
  utility_interfaces__srv__GetObjectPose_Event__fini(message_memory);
}

size_t utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__size_function__GetObjectPose_Event__request(
  const void * untyped_member)
{
  const utility_interfaces__srv__GetObjectPose_Request__Sequence * member =
    (const utility_interfaces__srv__GetObjectPose_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_const_function__GetObjectPose_Event__request(
  const void * untyped_member, size_t index)
{
  const utility_interfaces__srv__GetObjectPose_Request__Sequence * member =
    (const utility_interfaces__srv__GetObjectPose_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_function__GetObjectPose_Event__request(
  void * untyped_member, size_t index)
{
  utility_interfaces__srv__GetObjectPose_Request__Sequence * member =
    (utility_interfaces__srv__GetObjectPose_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__fetch_function__GetObjectPose_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const utility_interfaces__srv__GetObjectPose_Request * item =
    ((const utility_interfaces__srv__GetObjectPose_Request *)
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_const_function__GetObjectPose_Event__request(untyped_member, index));
  utility_interfaces__srv__GetObjectPose_Request * value =
    (utility_interfaces__srv__GetObjectPose_Request *)(untyped_value);
  *value = *item;
}

void utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__assign_function__GetObjectPose_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  utility_interfaces__srv__GetObjectPose_Request * item =
    ((utility_interfaces__srv__GetObjectPose_Request *)
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_function__GetObjectPose_Event__request(untyped_member, index));
  const utility_interfaces__srv__GetObjectPose_Request * value =
    (const utility_interfaces__srv__GetObjectPose_Request *)(untyped_value);
  *item = *value;
}

bool utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__resize_function__GetObjectPose_Event__request(
  void * untyped_member, size_t size)
{
  utility_interfaces__srv__GetObjectPose_Request__Sequence * member =
    (utility_interfaces__srv__GetObjectPose_Request__Sequence *)(untyped_member);
  utility_interfaces__srv__GetObjectPose_Request__Sequence__fini(member);
  return utility_interfaces__srv__GetObjectPose_Request__Sequence__init(member, size);
}

size_t utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__size_function__GetObjectPose_Event__response(
  const void * untyped_member)
{
  const utility_interfaces__srv__GetObjectPose_Response__Sequence * member =
    (const utility_interfaces__srv__GetObjectPose_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_const_function__GetObjectPose_Event__response(
  const void * untyped_member, size_t index)
{
  const utility_interfaces__srv__GetObjectPose_Response__Sequence * member =
    (const utility_interfaces__srv__GetObjectPose_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_function__GetObjectPose_Event__response(
  void * untyped_member, size_t index)
{
  utility_interfaces__srv__GetObjectPose_Response__Sequence * member =
    (utility_interfaces__srv__GetObjectPose_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__fetch_function__GetObjectPose_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const utility_interfaces__srv__GetObjectPose_Response * item =
    ((const utility_interfaces__srv__GetObjectPose_Response *)
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_const_function__GetObjectPose_Event__response(untyped_member, index));
  utility_interfaces__srv__GetObjectPose_Response * value =
    (utility_interfaces__srv__GetObjectPose_Response *)(untyped_value);
  *value = *item;
}

void utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__assign_function__GetObjectPose_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  utility_interfaces__srv__GetObjectPose_Response * item =
    ((utility_interfaces__srv__GetObjectPose_Response *)
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_function__GetObjectPose_Event__response(untyped_member, index));
  const utility_interfaces__srv__GetObjectPose_Response * value =
    (const utility_interfaces__srv__GetObjectPose_Response *)(untyped_value);
  *item = *value;
}

bool utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__resize_function__GetObjectPose_Event__response(
  void * untyped_member, size_t size)
{
  utility_interfaces__srv__GetObjectPose_Response__Sequence * member =
    (utility_interfaces__srv__GetObjectPose_Response__Sequence *)(untyped_member);
  utility_interfaces__srv__GetObjectPose_Response__Sequence__fini(member);
  return utility_interfaces__srv__GetObjectPose_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(utility_interfaces__srv__GetObjectPose_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(utility_interfaces__srv__GetObjectPose_Event, request),  // bytes offset in struct
    NULL,  // default value
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__size_function__GetObjectPose_Event__request,  // size() function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_const_function__GetObjectPose_Event__request,  // get_const(index) function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_function__GetObjectPose_Event__request,  // get(index) function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__fetch_function__GetObjectPose_Event__request,  // fetch(index, &value) function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__assign_function__GetObjectPose_Event__request,  // assign(index, value) function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__resize_function__GetObjectPose_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(utility_interfaces__srv__GetObjectPose_Event, response),  // bytes offset in struct
    NULL,  // default value
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__size_function__GetObjectPose_Event__response,  // size() function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_const_function__GetObjectPose_Event__response,  // get_const(index) function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__get_function__GetObjectPose_Event__response,  // get(index) function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__fetch_function__GetObjectPose_Event__response,  // fetch(index, &value) function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__assign_function__GetObjectPose_Event__response,  // assign(index, value) function pointer
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__resize_function__GetObjectPose_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_members = {
  "utility_interfaces__srv",  // message namespace
  "GetObjectPose_Event",  // message name
  3,  // number of fields
  sizeof(utility_interfaces__srv__GetObjectPose_Event),
  false,  // has_any_key_member_
  utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_member_array,  // message members
  utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_type_support_handle = {
  0,
  &utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_members,
  get_message_typesupport_handle_function,
  &utility_interfaces__srv__GetObjectPose_Event__get_type_hash,
  &utility_interfaces__srv__GetObjectPose_Event__get_type_description,
  &utility_interfaces__srv__GetObjectPose_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_utility_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Event)() {
  utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Request)();
  utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Response)();
  if (!utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_type_support_handle.typesupport_identifier) {
    utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "utility_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_service_members = {
  "utility_interfaces__srv",  // service namespace
  "GetObjectPose",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_type_support_handle,
  NULL,  // response message
  // utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_type_support_handle
  NULL  // event_message
  // utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_type_support_handle
};


static rosidl_service_type_support_t utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_service_type_support_handle = {
  0,
  &utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_service_members,
  get_service_typesupport_handle_function,
  &utility_interfaces__srv__GetObjectPose_Request__rosidl_typesupport_introspection_c__GetObjectPose_Request_message_type_support_handle,
  &utility_interfaces__srv__GetObjectPose_Response__rosidl_typesupport_introspection_c__GetObjectPose_Response_message_type_support_handle,
  &utility_interfaces__srv__GetObjectPose_Event__rosidl_typesupport_introspection_c__GetObjectPose_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    utility_interfaces,
    srv,
    GetObjectPose
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    utility_interfaces,
    srv,
    GetObjectPose
  ),
  &utility_interfaces__srv__GetObjectPose__get_type_hash,
  &utility_interfaces__srv__GetObjectPose__get_type_description,
  &utility_interfaces__srv__GetObjectPose__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_utility_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose)(void) {
  if (!utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_service_type_support_handle.typesupport_identifier) {
    utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, utility_interfaces, srv, GetObjectPose_Event)()->data;
  }

  return &utility_interfaces__srv__detail__get_object_pose__rosidl_typesupport_introspection_c__GetObjectPose_service_type_support_handle;
}

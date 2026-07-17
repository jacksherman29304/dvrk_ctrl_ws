// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from utility_interfaces:srv/GetObjectPose.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "utility_interfaces/srv/detail/get_object_pose__functions.h"
#include "utility_interfaces/srv/detail/get_object_pose__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace utility_interfaces
{

namespace srv
{

namespace rosidl_typesupport_introspection_cpp
{

void GetObjectPose_Request_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) utility_interfaces::srv::GetObjectPose_Request(_init);
}

void GetObjectPose_Request_fini_function(void * message_memory)
{
  auto typed_message = static_cast<utility_interfaces::srv::GetObjectPose_Request *>(message_memory);
  typed_message->~GetObjectPose_Request();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember GetObjectPose_Request_message_member_array[1] = {
  {
    "object_name",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(utility_interfaces::srv::GetObjectPose_Request, object_name),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers GetObjectPose_Request_message_members = {
  "utility_interfaces::srv",  // message namespace
  "GetObjectPose_Request",  // message name
  1,  // number of fields
  sizeof(utility_interfaces::srv::GetObjectPose_Request),
  false,  // has_any_key_member_
  GetObjectPose_Request_message_member_array,  // message members
  GetObjectPose_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  GetObjectPose_Request_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t GetObjectPose_Request_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &GetObjectPose_Request_message_members,
  get_message_typesupport_handle_function,
  &utility_interfaces__srv__GetObjectPose_Request__get_type_hash,
  &utility_interfaces__srv__GetObjectPose_Request__get_type_description,
  &utility_interfaces__srv__GetObjectPose_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace srv

}  // namespace utility_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<utility_interfaces::srv::GetObjectPose_Request>()
{
  return &::utility_interfaces::srv::rosidl_typesupport_introspection_cpp::GetObjectPose_Request_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, utility_interfaces, srv, GetObjectPose_Request)() {
  return &::utility_interfaces::srv::rosidl_typesupport_introspection_cpp::GetObjectPose_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__functions.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace utility_interfaces
{

namespace srv
{

namespace rosidl_typesupport_introspection_cpp
{

void GetObjectPose_Response_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) utility_interfaces::srv::GetObjectPose_Response(_init);
}

void GetObjectPose_Response_fini_function(void * message_memory)
{
  auto typed_message = static_cast<utility_interfaces::srv::GetObjectPose_Response *>(message_memory);
  typed_message->~GetObjectPose_Response();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember GetObjectPose_Response_message_member_array[2] = {
  {
    "pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Pose>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(utility_interfaces::srv::GetObjectPose_Response, pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "success",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(utility_interfaces::srv::GetObjectPose_Response, success),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers GetObjectPose_Response_message_members = {
  "utility_interfaces::srv",  // message namespace
  "GetObjectPose_Response",  // message name
  2,  // number of fields
  sizeof(utility_interfaces::srv::GetObjectPose_Response),
  false,  // has_any_key_member_
  GetObjectPose_Response_message_member_array,  // message members
  GetObjectPose_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  GetObjectPose_Response_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t GetObjectPose_Response_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &GetObjectPose_Response_message_members,
  get_message_typesupport_handle_function,
  &utility_interfaces__srv__GetObjectPose_Response__get_type_hash,
  &utility_interfaces__srv__GetObjectPose_Response__get_type_description,
  &utility_interfaces__srv__GetObjectPose_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace srv

}  // namespace utility_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<utility_interfaces::srv::GetObjectPose_Response>()
{
  return &::utility_interfaces::srv::rosidl_typesupport_introspection_cpp::GetObjectPose_Response_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, utility_interfaces, srv, GetObjectPose_Response)() {
  return &::utility_interfaces::srv::rosidl_typesupport_introspection_cpp::GetObjectPose_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__functions.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace utility_interfaces
{

namespace srv
{

namespace rosidl_typesupport_introspection_cpp
{

void GetObjectPose_Event_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) utility_interfaces::srv::GetObjectPose_Event(_init);
}

void GetObjectPose_Event_fini_function(void * message_memory)
{
  auto typed_message = static_cast<utility_interfaces::srv::GetObjectPose_Event *>(message_memory);
  typed_message->~GetObjectPose_Event();
}

size_t size_function__GetObjectPose_Event__request(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<utility_interfaces::srv::GetObjectPose_Request> *>(untyped_member);
  return member->size();
}

const void * get_const_function__GetObjectPose_Event__request(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<utility_interfaces::srv::GetObjectPose_Request> *>(untyped_member);
  return &member[index];
}

void * get_function__GetObjectPose_Event__request(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<utility_interfaces::srv::GetObjectPose_Request> *>(untyped_member);
  return &member[index];
}

void fetch_function__GetObjectPose_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const utility_interfaces::srv::GetObjectPose_Request *>(
    get_const_function__GetObjectPose_Event__request(untyped_member, index));
  auto & value = *reinterpret_cast<utility_interfaces::srv::GetObjectPose_Request *>(untyped_value);
  value = item;
}

void assign_function__GetObjectPose_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<utility_interfaces::srv::GetObjectPose_Request *>(
    get_function__GetObjectPose_Event__request(untyped_member, index));
  const auto & value = *reinterpret_cast<const utility_interfaces::srv::GetObjectPose_Request *>(untyped_value);
  item = value;
}

void resize_function__GetObjectPose_Event__request(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<utility_interfaces::srv::GetObjectPose_Request> *>(untyped_member);
  member->resize(size);
}

size_t size_function__GetObjectPose_Event__response(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<utility_interfaces::srv::GetObjectPose_Response> *>(untyped_member);
  return member->size();
}

const void * get_const_function__GetObjectPose_Event__response(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<utility_interfaces::srv::GetObjectPose_Response> *>(untyped_member);
  return &member[index];
}

void * get_function__GetObjectPose_Event__response(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<utility_interfaces::srv::GetObjectPose_Response> *>(untyped_member);
  return &member[index];
}

void fetch_function__GetObjectPose_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const utility_interfaces::srv::GetObjectPose_Response *>(
    get_const_function__GetObjectPose_Event__response(untyped_member, index));
  auto & value = *reinterpret_cast<utility_interfaces::srv::GetObjectPose_Response *>(untyped_value);
  value = item;
}

void assign_function__GetObjectPose_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<utility_interfaces::srv::GetObjectPose_Response *>(
    get_function__GetObjectPose_Event__response(untyped_member, index));
  const auto & value = *reinterpret_cast<const utility_interfaces::srv::GetObjectPose_Response *>(untyped_value);
  item = value;
}

void resize_function__GetObjectPose_Event__response(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<utility_interfaces::srv::GetObjectPose_Response> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember GetObjectPose_Event_message_member_array[3] = {
  {
    "info",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<service_msgs::msg::ServiceEventInfo>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(utility_interfaces::srv::GetObjectPose_Event, info),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "request",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<utility_interfaces::srv::GetObjectPose_Request>(),  // members of sub message
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(utility_interfaces::srv::GetObjectPose_Event, request),  // bytes offset in struct
    nullptr,  // default value
    size_function__GetObjectPose_Event__request,  // size() function pointer
    get_const_function__GetObjectPose_Event__request,  // get_const(index) function pointer
    get_function__GetObjectPose_Event__request,  // get(index) function pointer
    fetch_function__GetObjectPose_Event__request,  // fetch(index, &value) function pointer
    assign_function__GetObjectPose_Event__request,  // assign(index, value) function pointer
    resize_function__GetObjectPose_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<utility_interfaces::srv::GetObjectPose_Response>(),  // members of sub message
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(utility_interfaces::srv::GetObjectPose_Event, response),  // bytes offset in struct
    nullptr,  // default value
    size_function__GetObjectPose_Event__response,  // size() function pointer
    get_const_function__GetObjectPose_Event__response,  // get_const(index) function pointer
    get_function__GetObjectPose_Event__response,  // get(index) function pointer
    fetch_function__GetObjectPose_Event__response,  // fetch(index, &value) function pointer
    assign_function__GetObjectPose_Event__response,  // assign(index, value) function pointer
    resize_function__GetObjectPose_Event__response  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers GetObjectPose_Event_message_members = {
  "utility_interfaces::srv",  // message namespace
  "GetObjectPose_Event",  // message name
  3,  // number of fields
  sizeof(utility_interfaces::srv::GetObjectPose_Event),
  false,  // has_any_key_member_
  GetObjectPose_Event_message_member_array,  // message members
  GetObjectPose_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  GetObjectPose_Event_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t GetObjectPose_Event_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &GetObjectPose_Event_message_members,
  get_message_typesupport_handle_function,
  &utility_interfaces__srv__GetObjectPose_Event__get_type_hash,
  &utility_interfaces__srv__GetObjectPose_Event__get_type_description,
  &utility_interfaces__srv__GetObjectPose_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace srv

}  // namespace utility_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<utility_interfaces::srv::GetObjectPose_Event>()
{
  return &::utility_interfaces::srv::rosidl_typesupport_introspection_cpp::GetObjectPose_Event_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, utility_interfaces, srv, GetObjectPose_Event)() {
  return &::utility_interfaces::srv::rosidl_typesupport_introspection_cpp::GetObjectPose_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__functions.h"
// already included above
// #include "utility_interfaces/srv/detail/get_object_pose__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/service_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/service_type_support_decl.hpp"

namespace utility_interfaces
{

namespace srv
{

namespace rosidl_typesupport_introspection_cpp
{

// this is intentionally not const to allow initialization later to prevent an initialization race
static ::rosidl_typesupport_introspection_cpp::ServiceMembers GetObjectPose_service_members = {
  "utility_interfaces::srv",  // service namespace
  "GetObjectPose",  // service name
  // the following fields are initialized below on first access
  // see get_service_type_support_handle<utility_interfaces::srv::GetObjectPose>()
  nullptr,  // request message
  nullptr,  // response message
  nullptr,  // event message
};

static const rosidl_service_type_support_t GetObjectPose_service_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &GetObjectPose_service_members,
  get_service_typesupport_handle_function,
  ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<utility_interfaces::srv::GetObjectPose_Request>(),
  ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<utility_interfaces::srv::GetObjectPose_Response>(),
  ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<utility_interfaces::srv::GetObjectPose_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<utility_interfaces::srv::GetObjectPose>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<utility_interfaces::srv::GetObjectPose>,
  &utility_interfaces__srv__GetObjectPose__get_type_hash,
  &utility_interfaces__srv__GetObjectPose__get_type_description,
  &utility_interfaces__srv__GetObjectPose__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace srv

}  // namespace utility_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<utility_interfaces::srv::GetObjectPose>()
{
  // get a handle to the value to be returned
  auto service_type_support =
    &::utility_interfaces::srv::rosidl_typesupport_introspection_cpp::GetObjectPose_service_type_support_handle;
  // get a non-const and properly typed version of the data void *
  auto service_members = const_cast<::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
    static_cast<const ::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
      service_type_support->data));
  // make sure all of the service_members are initialized
  // if they are not, initialize them
  if (
    service_members->request_members_ == nullptr ||
    service_members->response_members_ == nullptr ||
    service_members->event_members_ == nullptr)
  {
    // initialize the request_members_ with the static function from the external library
    service_members->request_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::utility_interfaces::srv::GetObjectPose_Request
      >()->data
      );
    // initialize the response_members_ with the static function from the external library
    service_members->response_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::utility_interfaces::srv::GetObjectPose_Response
      >()->data
      );
    // initialize the event_members_ with the static function from the external library
    service_members->event_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::utility_interfaces::srv::GetObjectPose_Event
      >()->data
      );
  }
  // finally return the properly initialized service_type_support handle
  return service_type_support;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, utility_interfaces, srv, GetObjectPose)() {
  return ::rosidl_typesupport_introspection_cpp::get_service_type_support_handle<utility_interfaces::srv::GetObjectPose>();
}

#ifdef __cplusplus
}
#endif

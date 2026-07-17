// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from utility_interfaces:srv/GetObjectPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "utility_interfaces/srv/get_object_pose.hpp"


#ifndef UTILITY_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__BUILDER_HPP_
#define UTILITY_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "utility_interfaces/srv/detail/get_object_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace utility_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetObjectPose_Request_object_name
{
public:
  Init_GetObjectPose_Request_object_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::utility_interfaces::srv::GetObjectPose_Request object_name(::utility_interfaces::srv::GetObjectPose_Request::_object_name_type arg)
  {
    msg_.object_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::utility_interfaces::srv::GetObjectPose_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::utility_interfaces::srv::GetObjectPose_Request>()
{
  return utility_interfaces::srv::builder::Init_GetObjectPose_Request_object_name();
}

}  // namespace utility_interfaces


namespace utility_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetObjectPose_Response_success
{
public:
  explicit Init_GetObjectPose_Response_success(::utility_interfaces::srv::GetObjectPose_Response & msg)
  : msg_(msg)
  {}
  ::utility_interfaces::srv::GetObjectPose_Response success(::utility_interfaces::srv::GetObjectPose_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::utility_interfaces::srv::GetObjectPose_Response msg_;
};

class Init_GetObjectPose_Response_pose
{
public:
  Init_GetObjectPose_Response_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetObjectPose_Response_success pose(::utility_interfaces::srv::GetObjectPose_Response::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_GetObjectPose_Response_success(msg_);
  }

private:
  ::utility_interfaces::srv::GetObjectPose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::utility_interfaces::srv::GetObjectPose_Response>()
{
  return utility_interfaces::srv::builder::Init_GetObjectPose_Response_pose();
}

}  // namespace utility_interfaces


namespace utility_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetObjectPose_Event_response
{
public:
  explicit Init_GetObjectPose_Event_response(::utility_interfaces::srv::GetObjectPose_Event & msg)
  : msg_(msg)
  {}
  ::utility_interfaces::srv::GetObjectPose_Event response(::utility_interfaces::srv::GetObjectPose_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::utility_interfaces::srv::GetObjectPose_Event msg_;
};

class Init_GetObjectPose_Event_request
{
public:
  explicit Init_GetObjectPose_Event_request(::utility_interfaces::srv::GetObjectPose_Event & msg)
  : msg_(msg)
  {}
  Init_GetObjectPose_Event_response request(::utility_interfaces::srv::GetObjectPose_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GetObjectPose_Event_response(msg_);
  }

private:
  ::utility_interfaces::srv::GetObjectPose_Event msg_;
};

class Init_GetObjectPose_Event_info
{
public:
  Init_GetObjectPose_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetObjectPose_Event_request info(::utility_interfaces::srv::GetObjectPose_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GetObjectPose_Event_request(msg_);
  }

private:
  ::utility_interfaces::srv::GetObjectPose_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::utility_interfaces::srv::GetObjectPose_Event>()
{
  return utility_interfaces::srv::builder::Init_GetObjectPose_Event_info();
}

}  // namespace utility_interfaces

#endif  // UTILITY_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__BUILDER_HPP_

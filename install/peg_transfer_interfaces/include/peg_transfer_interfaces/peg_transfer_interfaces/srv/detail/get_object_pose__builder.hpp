// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from peg_transfer_interfaces:srv/GetObjectPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "peg_transfer_interfaces/srv/get_object_pose.hpp"


#ifndef PEG_TRANSFER_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__BUILDER_HPP_
#define PEG_TRANSFER_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "peg_transfer_interfaces/srv/detail/get_object_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace peg_transfer_interfaces
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
  ::peg_transfer_interfaces::srv::GetObjectPose_Request object_name(::peg_transfer_interfaces::srv::GetObjectPose_Request::_object_name_type arg)
  {
    msg_.object_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::peg_transfer_interfaces::srv::GetObjectPose_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::peg_transfer_interfaces::srv::GetObjectPose_Request>()
{
  return peg_transfer_interfaces::srv::builder::Init_GetObjectPose_Request_object_name();
}

}  // namespace peg_transfer_interfaces


namespace peg_transfer_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetObjectPose_Response_success
{
public:
  explicit Init_GetObjectPose_Response_success(::peg_transfer_interfaces::srv::GetObjectPose_Response & msg)
  : msg_(msg)
  {}
  ::peg_transfer_interfaces::srv::GetObjectPose_Response success(::peg_transfer_interfaces::srv::GetObjectPose_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::peg_transfer_interfaces::srv::GetObjectPose_Response msg_;
};

class Init_GetObjectPose_Response_pose
{
public:
  Init_GetObjectPose_Response_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetObjectPose_Response_success pose(::peg_transfer_interfaces::srv::GetObjectPose_Response::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_GetObjectPose_Response_success(msg_);
  }

private:
  ::peg_transfer_interfaces::srv::GetObjectPose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::peg_transfer_interfaces::srv::GetObjectPose_Response>()
{
  return peg_transfer_interfaces::srv::builder::Init_GetObjectPose_Response_pose();
}

}  // namespace peg_transfer_interfaces


namespace peg_transfer_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetObjectPose_Event_response
{
public:
  explicit Init_GetObjectPose_Event_response(::peg_transfer_interfaces::srv::GetObjectPose_Event & msg)
  : msg_(msg)
  {}
  ::peg_transfer_interfaces::srv::GetObjectPose_Event response(::peg_transfer_interfaces::srv::GetObjectPose_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::peg_transfer_interfaces::srv::GetObjectPose_Event msg_;
};

class Init_GetObjectPose_Event_request
{
public:
  explicit Init_GetObjectPose_Event_request(::peg_transfer_interfaces::srv::GetObjectPose_Event & msg)
  : msg_(msg)
  {}
  Init_GetObjectPose_Event_response request(::peg_transfer_interfaces::srv::GetObjectPose_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GetObjectPose_Event_response(msg_);
  }

private:
  ::peg_transfer_interfaces::srv::GetObjectPose_Event msg_;
};

class Init_GetObjectPose_Event_info
{
public:
  Init_GetObjectPose_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetObjectPose_Event_request info(::peg_transfer_interfaces::srv::GetObjectPose_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GetObjectPose_Event_request(msg_);
  }

private:
  ::peg_transfer_interfaces::srv::GetObjectPose_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::peg_transfer_interfaces::srv::GetObjectPose_Event>()
{
  return peg_transfer_interfaces::srv::builder::Init_GetObjectPose_Event_info();
}

}  // namespace peg_transfer_interfaces

#endif  // PEG_TRANSFER_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__BUILDER_HPP_

// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from utility_interfaces:srv/GetObjectPose.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "utility_interfaces/srv/get_object_pose.hpp"


#ifndef UTILITY_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__TRAITS_HPP_
#define UTILITY_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "utility_interfaces/srv/detail/get_object_pose__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace utility_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetObjectPose_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: object_name
  {
    out << "object_name: ";
    rosidl_generator_traits::value_to_yaml(msg.object_name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetObjectPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: object_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_name: ";
    rosidl_generator_traits::value_to_yaml(msg.object_name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetObjectPose_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace utility_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use utility_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const utility_interfaces::srv::GetObjectPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  utility_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use utility_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const utility_interfaces::srv::GetObjectPose_Request & msg)
{
  return utility_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<utility_interfaces::srv::GetObjectPose_Request>()
{
  return "utility_interfaces::srv::GetObjectPose_Request";
}

template<>
inline const char * name<utility_interfaces::srv::GetObjectPose_Request>()
{
  return "utility_interfaces/srv/GetObjectPose_Request";
}

template<>
struct has_fixed_size<utility_interfaces::srv::GetObjectPose_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<utility_interfaces::srv::GetObjectPose_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<utility_interfaces::srv::GetObjectPose_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace utility_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetObjectPose_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetObjectPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetObjectPose_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace utility_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use utility_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const utility_interfaces::srv::GetObjectPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  utility_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use utility_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const utility_interfaces::srv::GetObjectPose_Response & msg)
{
  return utility_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<utility_interfaces::srv::GetObjectPose_Response>()
{
  return "utility_interfaces::srv::GetObjectPose_Response";
}

template<>
inline const char * name<utility_interfaces::srv::GetObjectPose_Response>()
{
  return "utility_interfaces/srv/GetObjectPose_Response";
}

template<>
struct has_fixed_size<utility_interfaces::srv::GetObjectPose_Response>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Pose>::value> {};

template<>
struct has_bounded_size<utility_interfaces::srv::GetObjectPose_Response>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Pose>::value> {};

template<>
struct is_message<utility_interfaces::srv::GetObjectPose_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace utility_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetObjectPose_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetObjectPose_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetObjectPose_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace utility_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use utility_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const utility_interfaces::srv::GetObjectPose_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  utility_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use utility_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const utility_interfaces::srv::GetObjectPose_Event & msg)
{
  return utility_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<utility_interfaces::srv::GetObjectPose_Event>()
{
  return "utility_interfaces::srv::GetObjectPose_Event";
}

template<>
inline const char * name<utility_interfaces::srv::GetObjectPose_Event>()
{
  return "utility_interfaces/srv/GetObjectPose_Event";
}

template<>
struct has_fixed_size<utility_interfaces::srv::GetObjectPose_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<utility_interfaces::srv::GetObjectPose_Event>
  : std::integral_constant<bool, has_bounded_size<service_msgs::msg::ServiceEventInfo>::value && has_bounded_size<utility_interfaces::srv::GetObjectPose_Request>::value && has_bounded_size<utility_interfaces::srv::GetObjectPose_Response>::value> {};

template<>
struct is_message<utility_interfaces::srv::GetObjectPose_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<utility_interfaces::srv::GetObjectPose>()
{
  return "utility_interfaces::srv::GetObjectPose";
}

template<>
inline const char * name<utility_interfaces::srv::GetObjectPose>()
{
  return "utility_interfaces/srv/GetObjectPose";
}

template<>
struct has_fixed_size<utility_interfaces::srv::GetObjectPose>
  : std::integral_constant<
    bool,
    has_fixed_size<utility_interfaces::srv::GetObjectPose_Request>::value &&
    has_fixed_size<utility_interfaces::srv::GetObjectPose_Response>::value
  >
{
};

template<>
struct has_bounded_size<utility_interfaces::srv::GetObjectPose>
  : std::integral_constant<
    bool,
    has_bounded_size<utility_interfaces::srv::GetObjectPose_Request>::value &&
    has_bounded_size<utility_interfaces::srv::GetObjectPose_Response>::value
  >
{
};

template<>
struct is_service<utility_interfaces::srv::GetObjectPose>
  : std::true_type
{
};

template<>
struct is_service_request<utility_interfaces::srv::GetObjectPose_Request>
  : std::true_type
{
};

template<>
struct is_service_response<utility_interfaces::srv::GetObjectPose_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // UTILITY_INTERFACES__SRV__DETAIL__GET_OBJECT_POSE__TRAITS_HPP_

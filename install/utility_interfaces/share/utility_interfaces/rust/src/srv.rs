#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to utility_interfaces__srv__GetObjectPose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetObjectPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub object_name: std::string::String,

}



impl Default for GetObjectPose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetObjectPose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetObjectPose_Request {
  type RmwMsg = super::srv::rmw::GetObjectPose_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        object_name: msg.object_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        object_name: msg.object_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      object_name: msg.object_name.to_string(),
    }
  }
}


// Corresponds to utility_interfaces__srv__GetObjectPose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetObjectPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetObjectPose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetObjectPose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetObjectPose_Response {
  type RmwMsg = super::srv::rmw::GetObjectPose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      success: msg.success,
    }
  }
}






#[link(name = "utility_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__utility_interfaces__srv__GetObjectPose() -> *const std::ffi::c_void;
}

// Corresponds to utility_interfaces__srv__GetObjectPose
#[allow(missing_docs, non_camel_case_types)]
pub struct GetObjectPose;

impl rosidl_runtime_rs::Service for GetObjectPose {
    type Request = GetObjectPose_Request;
    type Response = GetObjectPose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__utility_interfaces__srv__GetObjectPose() }
    }
}



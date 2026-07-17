#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "utility_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__utility_interfaces__srv__GetObjectPose_Request() -> *const std::ffi::c_void;
}

#[link(name = "utility_interfaces__rosidl_generator_c")]
extern "C" {
    fn utility_interfaces__srv__GetObjectPose_Request__init(msg: *mut GetObjectPose_Request) -> bool;
    fn utility_interfaces__srv__GetObjectPose_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetObjectPose_Request>, size: usize) -> bool;
    fn utility_interfaces__srv__GetObjectPose_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetObjectPose_Request>);
    fn utility_interfaces__srv__GetObjectPose_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetObjectPose_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetObjectPose_Request>) -> bool;
}

// Corresponds to utility_interfaces__srv__GetObjectPose_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetObjectPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub object_name: rosidl_runtime_rs::String,

}



impl Default for GetObjectPose_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !utility_interfaces__srv__GetObjectPose_Request__init(&mut msg as *mut _) {
        panic!("Call to utility_interfaces__srv__GetObjectPose_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetObjectPose_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { utility_interfaces__srv__GetObjectPose_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { utility_interfaces__srv__GetObjectPose_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { utility_interfaces__srv__GetObjectPose_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetObjectPose_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetObjectPose_Request where Self: Sized {
  const TYPE_NAME: &'static str = "utility_interfaces/srv/GetObjectPose_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__utility_interfaces__srv__GetObjectPose_Request() }
  }
}


#[link(name = "utility_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__utility_interfaces__srv__GetObjectPose_Response() -> *const std::ffi::c_void;
}

#[link(name = "utility_interfaces__rosidl_generator_c")]
extern "C" {
    fn utility_interfaces__srv__GetObjectPose_Response__init(msg: *mut GetObjectPose_Response) -> bool;
    fn utility_interfaces__srv__GetObjectPose_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetObjectPose_Response>, size: usize) -> bool;
    fn utility_interfaces__srv__GetObjectPose_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetObjectPose_Response>);
    fn utility_interfaces__srv__GetObjectPose_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetObjectPose_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetObjectPose_Response>) -> bool;
}

// Corresponds to utility_interfaces__srv__GetObjectPose_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetObjectPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::rmw::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetObjectPose_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !utility_interfaces__srv__GetObjectPose_Response__init(&mut msg as *mut _) {
        panic!("Call to utility_interfaces__srv__GetObjectPose_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetObjectPose_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { utility_interfaces__srv__GetObjectPose_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { utility_interfaces__srv__GetObjectPose_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { utility_interfaces__srv__GetObjectPose_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetObjectPose_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetObjectPose_Response where Self: Sized {
  const TYPE_NAME: &'static str = "utility_interfaces/srv/GetObjectPose_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__utility_interfaces__srv__GetObjectPose_Response() }
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



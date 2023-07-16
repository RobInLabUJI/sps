cmake_minimum_required(VERSION 3.0.2)
project(sps)


find_package(catkin REQUIRED COMPONENTS
  message_generation
  message_runtime
  geometry_msgs
  nav_msgs
  roscpp
  rviz
  tf
  urdf
  xacro
  actionlib
  std_msgs
  gazebo_ros
  gazebo_msgs
  cv_bridge
  image_transport
  sensor_msgs
  roslib
)


generate_messages(
   DEPENDENCIES
   std_msgs
   geometry_msgs
   gazebo_msgs

 )


catkin_package(
  CATKIN_DEPENDS roscpp
)



install(TARGETS
   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
   RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
 )


include (FindPkgConfig)
if (PKG_CONFIG_FOUND)
	pkg_check_modules(GAZEBO gazebo)
endif()


include_directories(${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})

find_package(Eigen3 REQUIRED)
include_directories(${Eigen_INCLUDE_DIRS})


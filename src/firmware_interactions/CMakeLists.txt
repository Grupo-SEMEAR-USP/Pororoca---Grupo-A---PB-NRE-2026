cmake_minimum_required(VERSION 3.8)
project(firmware_interactions)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(std_msgs REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

add_library(custom_motor_bridge SHARED
  src/custom_motor_bridge.cpp
)

target_include_directories(custom_motor_bridge PRIVATE include)

ament_target_dependencies(custom_motor_bridge
  rclcpp
  hardware_interface
  pluginlib
  std_msgs
)

pluginlib_export_plugin_description_file(hardware_interface custom_motor_bridge.xml)

install(
  TARGETS custom_motor_bridge
  DESTINATION lib
)

install(
  FILES custom_motor_bridge.xml
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

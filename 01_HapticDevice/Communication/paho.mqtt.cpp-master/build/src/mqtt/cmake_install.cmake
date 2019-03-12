# Install script for directory: D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "D:\01_Projekte\P_01_Soft_Tissue_Robotics\11_Demostrators\05_SummerSchool2019\01_HapticDevice\Communication\paho.mqtt.c-master\build\src\Debug")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/mqtt" TYPE FILE FILES
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/async_client.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/buffer_ref.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/buffer_view.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/callback.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/client.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/connect_options.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/delivery_token.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/disconnect_options.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/exception.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/iaction_listener.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/iasync_client.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/iclient_persistence.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/message.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/response_options.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/ssl_options.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/string_collection.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/thread_queue.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/token.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/topic.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/types.h"
    "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src/mqtt/will_options.h"
    )
endif()


# Install script for directory: D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/src

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
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/build/src/Debug/paho-mqttpp3-static.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/build/src/Release/paho-mqttpp3-static.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/build/src/MinSizeRel/paho-mqttpp3-static.lib")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/build/src/RelWithDebInfo/paho-mqttpp3-static.lib")
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("D:/01_Projekte/P_01_Soft_Tissue_Robotics/11_Demostrators/05_SummerSchool2019/01_HapticDevice/Communication/paho.mqtt.cpp-master/build/src/mqtt/cmake_install.cmake")

endif()


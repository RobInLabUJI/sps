FROM osrf/ros:noetic-desktop-full

RUN apt-get update && apt-get install -y \
      python-is-python3 \
      ros-noetic-teleop-twist-keyboard && \
    rm -rf /var/lib/apt/lists/*
    
RUN mkdir -p /catkin_ws/src/sps

COPY . /catkin_ws/src/sps

SHELL ["/bin/bash", "-c"]

RUN cd /catkin_ws \
 && source /opt/ros/noetic/setup.bash \
 && apt-get update \
 && rosdep install --from-paths src --ignore-src -r -y \
 && rm -rf /var/lib/apt/lists/*

RUN cd catkin_ws \
 && source /opt/ros/noetic/setup.bash \
 && catkin_make

RUN sed --in-place --expression \
      '$isource "/catkin_ws/devel/setup.bash"' \
      /ros_entrypoint.sh

# run launch file
CMD ["roslaunch", "sps", "sim.launch"]

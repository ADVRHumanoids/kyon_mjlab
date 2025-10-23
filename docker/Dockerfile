FROM ros:jazzy-ros-core

USER root

WORKDIR /root

RUN apt update && apt install -y python3-venv python3-pip git lsb-release cmake && \
    apt clean && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google-deepmind/mujoco_warp.git --recurse-submodules && \
    git clone https://github.com/mujocolab/mjlab.git --recurse-submodules

SHELL ["/bin/bash", "-ic"]

RUN python3 -m venv env && \
    source env/bin/activate && \
    echo source ~/env/bin/activate >> ~/.bashrc && \
    cd mujoco_warp && python -m pip install -e . && \
    cd ../mjlab && python -m pip install -e . && \
    python -m pip install onnxscript && \
    rm -rf ~/.cache/pip

RUN pip install hhcm-forest && \
    mkdir forest_ws && cd forest_ws && forest init && \
    source setup.bash && echo source $PWD/setup.bash >> ~/.bashrc && \
    forest add-recipes https://github.com/advrhumanoids/multidof_recipes.git -t ros2 

ENV HHCM_FOREST_CLONE_DEFAULT_PROTO=https

RUN echo source /opt/ros/jazzy/setup.bash >> ~/.bashrc

RUN apt update && apt install -y ros-$ROS_DISTRO-xacro ros-$ROS_DISTRO-srdfdom && \
    apt clean && rm -rf /var/lib/apt/lists/* && \ 
    pip install catkin_pkg rospkg && \
    rm -rf ~/.cache/pip

RUN --mount=type=secret,id=netrc,dst=/root/.netrc cd forest_ws && forest grow iit-kyon-ros-pkg --no-deps

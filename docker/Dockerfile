FROM ubuntu:24.04

USER root

WORKDIR /root

RUN apt update && apt install -y python3-venv python3-pip git && \
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

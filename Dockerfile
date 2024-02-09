FROM ubuntu:18.04

ARG OPENSSL_CONFIG
ARG OPENSSL_VERSION=1.1.1


RUN apt-get update -qq \
    && apt-get -y install \
    git \
    curl \
    build-essential \
    wget \
    libssl-dev \
    libcurl4-openssl-dev \
    liblog4cplus-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    streamer1.0-plugins-base-apps \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    python3 \
    && wget wget https://bootstrap.pypa.io/get-pip.py \
    && python3.7 get-pip.py \
    && pip install boto3

# Pre-built make
WORKDIR /tmp
RUN curl -sSL https://github.com/Kitware/CMake/releases/download/v3.10.0/cmake-3.10.0.tar.gz -o cmake-3.10.0.tar.gz \
    && tar -zxvf cmake-3.10.0.tar.gz \
    && cd cmake-3.10.0 \
    && ./bootstrap \
    && make -j 4 \
    && make install

# Clone the repo
WORKDIR /tmp
RUN git clone https://github.com/erickarana/amazon-kinesis-video-streams-producer-sdk-cpp.git
RUN cd amazon-kinesis-video-streams-producer-sdk-cpp && \
    mkdir build && \
    cd build && \
    cmake .. -DBUILD_GSTREAMER_PLUGIN=TRUE && make


RUN mkdir /home/workdir/
RUN mkdir /home/workdir/videos/

COPY ./videos/* /home/workdir/videos/
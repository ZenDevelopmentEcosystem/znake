FROM ubuntu:18.04

RUN \
    apt-get update && \
    apt-get --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install locales make python3 python3-venv software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

ADD k2 /opt/k2
ADD zaf /opt/zaf

ENV LANG=en_US.UTF-8
WORKDIR /opt/k2
RUN \
    touch requirements.txt && \
    make cleanup && \
    make prepare_node_local && \
    /opt/k2/.venv/bin/pip3 install /opt/zaf && \
    ln -s /opt/k2/.venv/bin/zk2 /usr/bin/zk2
FROM ubuntu:16.04

ENV DEBIAN_FRONTEND=noninteractive

RUN \
    apt-get update && \
    apt-get --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install python3 python3-venv python3-pip locales sudo gdebi texlive-base texlive-latex-extra && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

RUN echo "ALL ALL=NOPASSWD:ALL" >> /etc/sudoers

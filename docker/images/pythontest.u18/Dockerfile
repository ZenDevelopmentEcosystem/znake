FROM ubuntu:18.04

RUN \
    apt-get update && \
    apt-get --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install python3 python3-venv python3-pip locales sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

RUN echo "ALL ALL=NOPASSWD:ALL" >> /etc/sudoers
RUN rm -f /var/lib/dpkg/statoverride && touch /var/lib/dpkg/statoverride

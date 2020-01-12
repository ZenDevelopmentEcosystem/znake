FROM ubuntu:16.04

RUN \
    apt-get update && \
    apt-get --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install locales dpkg-dev debhelper dh-virtualenv python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

RUN \
    curl -LO "https://mirrors.edge.kernel.org/ubuntu/pool/universe/d/dh-virtualenv/dh-virtualenv_1.1-1_all.deb" && \
    dpkg --ignore-depends libjs-sphinxdoc,sphinx-rtd-theme-common -i dh-virtualenv_1.1-1_all.deb && \
    rm dh-virtualenv_1.1-1_all.deb

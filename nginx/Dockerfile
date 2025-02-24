FROM nginx:stable-bookworm

RUN apt-get update -qq &&\
    apt-get -qq install --no-install-recommends -y \
    curl \
    dnsutils \
    iproute2 \
    iputils-ping \
    telnet \
    traceroute &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

RUN printf "PS1='[\@]\u@\h(\$(hostname -i)):\w \n\\$ '" >> /root/.bashrc

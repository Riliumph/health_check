FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Selenium用にGoogle Chromeをaptで入れられる設定を入れる。
# ただし、aptでGoogle Chromeを入れるとエラーが発生するので手動で入れる
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -Lks https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -\
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get -qq update \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq install --no-install-recommends -y\
    # utility
    peco\
    silversearcher-ag\
    vim\
    git\
    # networks
    curl \
    dnsutils \
    iproute2 \
    iputils-ping \
    telnet \
    traceroute \
    && apt-get clean\
    && rm -rf /var/lib/apt/lists/*

# hadolint for docker
ARG HADOLINT_URL
RUN curl -Lks -o /usr/local/bin/hadolint ${HADOLINT_URL}\
    && chmod o+x /usr/local/bin/hadolint

# git
WORKDIR /usr/share/doc/git/contrib/diff-highlight
RUN make\
    && chmod o+x diff-highlight\
    && ln -s /usr/share/doc/git/contrib/diff-highlight/diff-highlight /usr/local/bin

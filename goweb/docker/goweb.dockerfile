FROM debian:bookworm-slim

USER root

RUN ls /etc/apt/
RUN sed -i 's\http://deb.debian.org/\http://mirrors.tuna.tsinghua.edu.cn/\' /etc/apt/sources.list.d/debian.sources

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -yy apt-transport-https eatmydata

# install required packages
RUN apt-get install -yy \
    wget \
    git

WORKDIR /tmp

# install go
RUN wget https://go.dev/dl/go1.22.5.linux-amd64.tar.gz && \
    rm -rf /usr/local/go && \
    tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz

ENV PATH=$PATH:/usr/local/go/bin

# run web server
RUN git clone https://github.com/PengJi/compute-go.git && \
    cd compute-go/goweb && \
    cp config/config.yaml /etc/ && \
    go env -w GO111MODULE=on && \
    go env -w GOPROXY=https://goproxy.cn,direct && \
    go build -o /usr/local/bin/webserver main.go

EXPOSE 8080
ENV GIN_MODE=release
CMD ["/usr/local/bin/webserver", "--config=/etc/"]

# docker build -f web.dockerfile -t registry.cn-beijing.aliyuncs.com/pengji/dev:web-debian12 .
# docker run -d -p 8081:8080 registry.cn-beijing.aliyuncs.com/pengji/dev:web-debian12

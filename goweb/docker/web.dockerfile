FROM debian:bookworm-slim

USER root

RUN sed -i 's\http://deb.debian.org/\http://mirrors.tuna.tsinghua.edu.cn/\' /etc/apt/sources.list

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
RUN git clone https://github.com/PengJi/kvmtool-rs.git && \
    cd kvmtool-rs/goweb && \
    go env -w GO111MODULE=on && \
    go env -w GOPROXY=https://goproxy.cn,direct && \
    go build -o /usr/local/bin/webserver main.go

EXPOSE 8080
ENV GIN_MODE=release
CMD ["/usr/local/bin/webserver"]

# docker build -f web.dockerfile -t registry.cn-beijing.aliyuncs.com/pengji/dev:web-debian12 .
# docker run -d -p 8081:8080 registry.cn-beijing.aliyuncs.com/pengji/dev:web-debian12

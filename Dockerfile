FROM ubuntu:18.04

ARG archive
ARG version=2020-02-14

ENV BINDIR /usr/local/bin
ENV OPENCORDIR /home/opencor

WORKDIR $OPENCORDIR
SHELL ["/bin/bash", "-c"]

RUN apt-get -qq update && apt-get install -y \
    curl \
    dos2unix \
    libpulse-mainloop-glib0 \
    libx11-6 \
    libxext6 \
    libxslt1.1 \
    sqlite3

COPY . $OPENCORDIR

RUN mkdir OpenCOR && \
    cd OpenCOR && \
    if [[ -n $archive ]]; then \
        tar --strip-components=1 -xzf ../$archive && \
        rm ../$archive ; \
    else \
        if [[ $version =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then \
            URL=https://opencor.ws/downloads/$version/OpenCOR-`sed 's/\./-/g' <<< $version`-Linux.tar.gz ; \
        else \
            URL=https://opencor.ws/downloads/snapshots/$version/OpenCOR-$version-Linux.tar.gz ; \
        fi && \
        curl $URL | tar --strip-components=1 -xz ; \
    fi

ENTRYPOINT ["entrypoint"]

COPY ./entrypoint $BINDIR
RUN dos2unix -q $BINDIR/entrypoint

FROM ubuntu:20.04

ARG archive
ARG version=0.7

ENV HOMEDIR /home/opencor
ENV OPENCORDIR $HOMEDIR/OpenCOR

WORKDIR $HOMEDIR
SHELL ["/bin/bash", "-c"]

RUN apt-get -qq update && apt-get install -y \
    curl \
    libglapi-mesa \
    libpulse-mainloop-glib0 \
    libx11-6 \
    libxext6 \
    libxslt1.1 \
    sqlite3

COPY . $HOMEDIR

RUN mkdir $OPENCORDIR && \
    cd $OPENCORDIR && \
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

ENV PATH "$OPENCORDIR:$PATH"

ENTRYPOINT ["pythonshell", "opencor.py"]

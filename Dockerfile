FROM python:3-alpine

# install phantomjs
RUN apt-get update \
  && apt-get upgrade -yqf \
  && apt-get install -yqq build-essential chrpath libssl-dev libxft-dev \
  && apt-get install -yqq libfreetype6 libfreetype6-dev \
  && apt-get install -yqq libfontconfig1 libfontconfig1-dev \
  && apt-get autoremove -yqq
RUN cd /tmp \
  && export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64" \
  && curl -L https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2 -o phantomjs.tar.bz2 \
  && mkdir -p phantomjs \
  && tar --bzip2 -xf phantomjs.tar.bz2 -C phantomjs --strip-components 1 \
  && mv phantomjs /usr/local/share \
  && chmod 755 /usr/local/share/phantomjs/bin/phantomjs \
  && ln -sf /usr/local/share/phantomjs/bin/phantomjs /usr/local/bin

# update pip and install python packages
RUN pip install pip -U --no-cache \
  && pip list --outdated | awk '{print $1}' | xargs pip install -U --no-cache
ADD requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# adding files
RUN mkdir -p /app/autoamex
ADD src/ /app/autoamex/src
WORKDIR /app/autoamex/src


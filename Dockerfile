FROM atreyo/docker-python-selenium-phantomjs
MAINTAINER yangmaoxiaozhan@gmail.com
RUN mkdir ~/autoamex
WORKDIR ~
RUN pwd
# ENTRYPOINT ["python ~/autoamex/src/autoamex.py"]

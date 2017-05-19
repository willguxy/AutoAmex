#!/bin/bash
docker run -d -v $(pwd):/autoamex \
    atreyo/docker-python-selenium-phantomjs \
    /bin/bash -c 'cd /autoamex/src; python autoamex.py phantomjs'

#!/bin/bash
docker run -d -v $(pwd):/autoamex \
    atreyo/docker-python-selenium-phantomjs \
    python /autoamex/src/autoamex.py phantomjs

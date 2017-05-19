#!/bin/bash
docker run -d -v $(pwd):/autoamex \
    atreyo/docker-python-selenium-phantomjs \
    /autoamex/src/autoamex.py 

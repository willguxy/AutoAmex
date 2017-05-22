#!/bin/bash
docker run -d -v $(pwd):/autoamex \
    sgrio/python-selenium \
    /bin/bash -c 'cd /autoamex/src; python autoamex.py chrome_linux'

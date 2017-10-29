IMAGE_NAME ?= autoamex

build:
	@docker build -t $(IMAGE_NAME):latest .

run:
	@docker run -d --name=autoamex \
	    -v $$(pwd)/tmp:/app/autoamex/tmp \
	    -v $$(pwd)/conf:/app/autoamex/conf \
	    $(IMAGE_NAME):latest python autoamex.py headless

log:
	@docker logs -f autoamex

clean:
	@find . -name \*.pyc -delete && \
	    docker ps -aq -f status=exited | xargs docker rm

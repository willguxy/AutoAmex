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
	@find . -type f -name "*.py[co]" -delete -print && \
	    find . -type d -name "__pycache__" -delete -print

clean-docker:
	@docker ps -aq -f status=exited | xargs docker rm

build:
	docker build -t autoamex:latest .

run:
	docker run -d -v $$(pwd):/usr/src/app/autoamex autoamex:latest \
  /bin/bash -c "cd autoamex/src; python autoamex.py headless"

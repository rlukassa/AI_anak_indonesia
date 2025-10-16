IMAGE  ?= myproject
NAME   ?= myproject
PORT   ?= 8000

.PHONY: build run stop

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm -it --name $(NAME) -p $(PORT):$(PORT) $(IMAGE)

stop:
	-docker stop $(NAME)

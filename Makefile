PROJECT_NAME ?= $(shell python3 setup.py --name)
PROJECT_VERSION ?= $(shell python3 setup.py --version)
PROJECT_NAMESPACE = 'camcoh1989'

all:
	@echo "make devenv	- Configure dev environment"
	@echo "make build	- Build docker image"
	@echo "make upload	- Build & upload docker image"
	@echo "make clean	- Remove files created by distutils & dev modules"
	@echo "make test	- Run tests"
	@exit 0

devenv:
	rm -rf env
	virtualenv env -p python3
	env/bin/pip install -Ue '.[develop]'

clean:
	rm -fr *.egg-info .tox dist

sdist: clean bump
	env/bin/python setup.py sdist

build: clean sdist
	docker build \
		-t ${PROJECT_NAMESPACE}/${PROJECT_NAME}:${PROJECT_VERSION} \
		-t ${PROJECT_NAMESPACE}/${PROJECT_NAME}:latest .

upload: build
	docker push ${PROJECT_NAMESPACE}/${PROJECT_NAME}:latest
	docker push ${PROJECT_NAMESPACE}/${PROJECT_NAME}:${PROJECT_VERSION}

test:
	env/bin/tox

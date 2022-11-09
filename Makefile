.PHONY: clean

VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;
VERSION := $(shell python3 -m myrt_desk_api.version)

SRC := \
	$(wildcard myrt_desk_api/*/*.py) \
	$(wildcard myrt_desk_api/*.py)

publish: clean dist/
	git tag "v$(VERSION)"
	git push --tags
	$(VENV) python3 -m twine upload --repository pypi dist/* -umishamyrt

install: clean dist/
	$(VENV) pip3 install .

install-system: dist/
	pip3 install .

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

configure: $(VENV_PATH)

lint:
	$(VENV) pylint ./myrt_desk_api ./bin

dist/: $(VENV_PATH) $(SRC)
	echo "$(VERSION)" > ".version"
	$(VENV) python3 setup.py sdist bdist_wheel

$(VENV_PATH):
	python3 -m venv $(VENV_PATH)
	$(VENV) pip3 install -r requirements.txt
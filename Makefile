.PHONY: clean

VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;
VERSION := 1.0.5
# $(shell python3.11 -m myrt_desk_api.version)

SRC := \
	$(wildcard myrt_desk_api/*/*.py) \
	$(wildcard myrt_desk_api/*.py)

publish: clean dist/
	git tag "v$(VERSION)"
	git push --tags
	$(VENV) python3.11 -m twine upload --repository pypi dist/* -umishamyrt

install: clean dist/
	$(VENV) pip install --disable-pip-version-check .

install-system: dist/
	pip3 install --disable-pip-version-check .

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

configure: $(VENV_PATH)
	make build
	make install

lint:
	$(VENV) pylint ./myrt_desk_api ./bin

dist/: $(VENV_PATH) $(SRC)
	echo "$(VERSION)" > ".version"
	$(VENV) python3.11 setup.py sdist bdist_wheel

$(VENV_PATH): requirements.txt
	rm -rf "$(VENV_PATH)"
	python3.11 -m venv "$(VENV_PATH)"
	$(VENV) pip3 install --disable-pip-version-check -r requirements.txt

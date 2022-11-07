

.PHONY: clean

VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;

SRC := \
	$(wildcard myrt_desk_api/*/*.py) \
	$(wildcard myrt_desk_api/*.py)

publish: dist/
	$(VENV) python3 -m twine upload --repository pypi dist/*

install: dist/
	$(VENV) pip3 install .

install-system: dist/
	pip3 install .

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

configure: $(VENV_PATH)

lint:
	$(VENV) pylint ./dohome_api

dist/: $(VENV_PATH) $(SRC)
	$(VENV) python3 setup.py sdist bdist_wheel

$(VENV_PATH):
	python3 -m venv $(VENV_PATH)
	$(VENV) pip3 install -r requirements.txt
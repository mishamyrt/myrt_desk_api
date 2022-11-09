

.PHONY: clean

VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;

SRC := \
	$(wildcard myrt_desk_api/*/*.py) \
	$(wildcard myrt_desk_api/*.py)

publish: clean dist/
	$(VENV) python3 -m twine upload --repository pypi dist/*

install: clean dist/
	$(VENV) pip3 install .

install-system: dist/
	pip3 install .

clean:
	rm -f *.egg-info
	rm -rf build
	rm -rf dist

configure: $(VENV_PATH)

lint:
	$(VENV) pylint ./myrt_desk_api ./bin

dist/: $(VENV_PATH) $(SRC)
	$(VENV) python3 setup.py sdist bdist_wheel

$(VENV_PATH):
	python3 -m venv $(VENV_PATH)
	$(VENV) pip3 install -r requirements.txt
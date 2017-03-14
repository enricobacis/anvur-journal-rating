.PHONY: all clean run

MAIN = extract.py
VENV = venv

all: run

run: $(VENV)
	$(VENV)/bin/python $(MAIN)

clean:
	rm -rf $(VENV)

$(VENV):
	virtualenv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

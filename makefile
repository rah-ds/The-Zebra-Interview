default:
	echo @ default

## builds the virtual environment and attaches it to the ipykernel to be used
build_venv:
	pip3 install --upgrade pip;
	python3.13 -m venv .venv;

add_library:
	source .venv/bin/activate && pip install -r requirements.txt;
	source .venv/bin/activate && pip install ipykernel;
	source .venv/bin/activate && python3.13 -m ipykernel install --user --name=.venv;

## install stuff not in requirements
install_extras: .venv
	source .venv/bin/activate && pip install nbqa nbconvert nbstripout;

## format and check notebooks
check_notebook: # assumes you're in the notebooks directory
	nbqa pylint *.ipynb;
	black *.ipynb;

## run the test folder
tests: 
	source .venv/bin/activate && pytest tests -vvx -p no:warnings

## runs Google Style Guide Linter
lint:
	pylint src/*.py

## runs black to auto format code
auto_format:
	black src/

## clean up the repo
clean:
	echo "add what files to clean up"


.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
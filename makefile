PY_VERSION_NUM = $(PY_VERSION_NUM)


default:
	echo @ makefile

env:
	pip install --upgrade pip;
	python$(PY_VERSION_NUM) -m venv env;
	source env/bin/activate && pip install -r requirements.txt;

install_kernel: env
	source env/bin/activate && python$(PY_VERSION_NUM) -m ipykernel --user --name env --display-name = "Python ($(PY_VERSION_NUM) env)"

install_extras: env
	source env/bin/activate && pip install nbqa nbconvert nbstripout

.PHONY: tests
tests: update
	source env/bin/activate; pytest -vvx tests/ 

can_export_to_pdfs: # note should probably be a script that gets called check for MAC
    brew install pandoc texlive-xetex texlive-fonts-recommended texlive-plain-generic

src: pylintrc
	black src/*
	pylint src/*
	
check_notebook: # assumes you're in the notebooks directory
	nbqa pylint *.ipynb
	black *.ipynb

# write rule that won't let me push without checking if the notebook doesn't have outputs saved


.PHONY: tests install_cosmicai lint format clean

# useful for debugging
# default:
# 	echo @ makefile

## builds the virtual environment and attaches it to the ipykernel to be used
build_venv:
	pip install --upgrade pip;
	python3.11 -m venv .venv;
	source .venv/bin/activate && pip install -r requirements.txt;
	source .venv/bin/activate && pip install ipykernel
	source .venv/bin/activate && python3.11 -m ipykernel install --user --name=.venv;

# boto is being weird
## runs the package tests
tests: # only non integration tests
	source .venv/bin/activate && pytest tests -vvx -p no:warnings

## updates the astronomy ai github
update_Astronomy_AI_git:
	cd AI-for-Astronomy && git pull

## install the prediction function to be used elsewhere
install_cosmicai:
	source .venv/bin/activate && pip install -e .

# only useful for markdown readme
generate_file_structure:
	tree -L 1

## runs Google Style Guide Linter
lint:
	pylint src/cosmicai/*.py

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
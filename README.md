# The Zebra Interview
<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

 Take Home Project For the Zebra Data Science interview

* GOAL: 6 hours of work to show off analysis, coding, and presentation
* Written In Python3.11, use the make file to build


## Repo Structure

```bash
├── LICENSE # MIT
├── README.md 
├── data # raw/ interim/ final/
├── docs # brief and presentation
├── makefile 
├── notebooks # work showing analysis
├── plots # plots used in presentation
├── pylintrc # Google Style Guide
├── requirements.txt # Python 3.11
├── scripts 
├── src 
└── tests # pytest
```



## Make

```bash
make <pick an option>
```

```yaml
# options
auto_format: runs black to auto format code 
build_venv: builds the virtual environment and attaches it to the ipykernel to be used 
check_notebook: format and check notebooks 
clean: clean up the repo 
install_extras : install stuff not in requirements 
lint: runs Google Style Guide Linter 
tests: run the test folder 
```
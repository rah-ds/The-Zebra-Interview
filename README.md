# The Zebra Interview
<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

# Take Home Project

## Objective

You are a data scientist for a top movie studio.

After a series of box office flops, the producers at your
studio are starting to question their strategy and need a new direction. 

You suggest a new approach -
using data to determine what factors go into making a successful film.

Luckily, you have a dataset of over 5,000 films to mine for insights! The producers ask you to analyze the
data and present a report detailing your findings and recommendations on revamping the studio’s
strategy.

## Data
Attached is The Zebra movie dataset for use.
**Data Dictionary (selected columns)**

* `num_critic_reviews` - number of movie reviews written by critics
* `num_user_reviews` - number of movie reviews written by IMDB users
* `num_users_voted` - number of IMDB users that rated the film
* `duration` - the length of the film in minutes
* `actor_n_facebook_likes` - the number of likes on the actor’s Facebook page (we can assume this was `measured before the film was released)
* `gross` - the film’s gross revenue
* `movie_score` - the film’s rating on a 1-10 scale by users that voted

### Goal
* only supposed to spend **6 hours** on this

### Planned Breakdown
* **1 hour** setup (power point starter and code set)
  * includes some basic time for understanding and research
* 3 key insights - **3 hours**, put each as own notebook
* what we could explore, next steps, code checking, **1 hour**
* presentation build and script build and practice **1 hours**


>[!NOTE]
> Written In Python3.11, use the make file to build, or install requirements directly


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
make <pick an option> # to run
brew install make # to install
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
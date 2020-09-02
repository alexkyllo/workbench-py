# Makefile
# This is an example Makefile to help you get familiar with GNU Make
# and get started with using it to automate your project build tasks.
# For the full GNU Make manual, see:
# https://www.gnu.org/software/make/manual/make.html
#
# A Makefile consists of rules, which take following form:
# target … : prerequisites …
#        recipe
#        …
#        …
#
# Multiple targets and prerequisites are separated by spaces;
# multiple recipes are separated by newlines.
#
# If the target file exists, and the file has not been modified since any
# of its prerequisite files were last modified, the rule will be skipped.
# This means that it won't redo any work that it doesn't need to!
#
# Some things to note:
# - Indentation must be tabs--Make will error if you use spaces.
# - To break a long line, use a backslash: \
# - If you just type "make" at the command line in the directory
# where the Makefile is, it will run the first recipe
# (after running its prerequisites).
# - Other than that, the ordering of the rules in the file doesn't matter.
# Make builds a dependency graph and performs a topological sort to determine
# the correct rule execution order.
# - If you type "make {rule name}" it will run that specific rule name
# (again, after running its prerequisites).
# - If you type "make -n" it will tell you what it's going to run without
# actually running it (a dry run).
#
# This includes your .env file variables in the Makefile
include .env
export

# Rules can either be file names (a rule for producing a file)
# or just task names that aren't files, called "phony rules."
# List any phony rules here so that Make knows not to look for
# files by these names:
.PHONY: style environment install data figures reports

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## One-time conda environment setup
environment:
	conda env create -f environment.yml || conda env update -f environment.yml
	@echo ">>> Conda env created. Activate with:\nconda activate $(REPO_NAME)"

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Format using black
fmt:
	black .

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## A rule to run all the project tasks
all: data models figures notebooks reports

## Render the HTML report
reports: reports/report.html

reports/report.html: notebooks/notebook.ipynb
	nbconvert $<

## Render the notebook from the Markdown file
notebooks: notebooks/notebook.ipynb

notebooks/notebook.ipynb: $(PACKAGE_NAME)/report.md
	jupytext $< $@ --execute

## Plot figures
figures: figures/scatter_plot.png

# A recipe for a data visualization.
figures/scatter_plot.png : $(PACKAGE_NAME)/plot.py data/processed/scored_data.csv
	$(PYTHON) $^ $@

## Train models
models: models/model.joblib

## Make Dataset
data: data/processed/train_data.csv

# A recipe for a processed data file.
# This recipe says that data/processed/processed_data.csv depends on
# {{ cookiecutter.package_name }}/clean.py and data/raw/raw_data.csv.
# The recipe to make it is running the clean.py script
# with the given arguments.
# $< is shorthand for "the first prerequisite in the list."
# $^ is all of the prerequisites in the list
# $@ is the target name
data/processed/train_data.csv: $(PACKAGE_NAME)/clean.py data/raw/raw_train_data.csv
	$(PYTHON) $^ $@ --fit

data/processed/test_data.csv: $(PACKAGE_NAME)/clean.py data/raw/raw_test_data.csv
	$(PYTHON) $^ $@

data/raw/raw_data.csv: $(PACKAGE_NAME)/get.py
	$(PYTHON) $< help Samples queries/query.csl \
$(BLOB_ACCOUNT) $(BLOB_CONTAINER) $(BLOB_KEY) $(REPO_NAME) raw_data \
data/raw/raw_data.csv

# A recipe for a trained, serialized ML model.
models/model.joblib: $(PACKAGE_NAME)/train.py data/processed/train_data.csv
	$(PYTHON) $^ $@

# A recipe for splitting raw data into train and test sets
data/raw/raw_test_data.csv data/raw/raw_train_data.csv &: $(PACKAGE_NAME)/split.py \
data/raw/raw_data.csv
	$(PYTHON) $^ data/raw/raw_test_data.csv data/raw/raw_train_data.csv

# A recipe for scoring the model on test data.
data/processed/scored_data.csv: $(PACKAGE_NAME)/score.py data/processed/test_data.csv
	$(PYTHON) $^ $@

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
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

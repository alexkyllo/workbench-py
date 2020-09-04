{{cookiecutter.repo_name}}
==============================

{{cookiecutter.description}}

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make models`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data/
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    ├── figures/           <- Generated plots and figures (saved as .png files)
    ├── models/            <- Trained and serialized models, model predictions, or model summaries
    ├── notebooks/         <- Jupyter notebooks.
    ├── pipelines/         <- Serialized scikit-learn data transformer pipelines.
    ├── references/        <- Data dictionaries, manuals, and all other explanatory materials.
    ├── reports            <- Generated analysis reports as HTML, PDF, etc.
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── {{ cookiecutter.package_name }}      <- Source code for use in this project.
    │   ├── __init__.py    <- Makes {{ cookiecutter.package_name }} a Python module
    │   ├── clean.py       <- Clean data in data/raw/ and output result to data/processed
    │   ├── explore.py     <- Exploratory data analysis script for interactive work
    │   ├── get.py         <- Script to get data from the source
    │   ├── matplotlibrc   <- Settings file for matplotlib plot styling
    │   ├── plot.py        <- Script to plot visuals and save to figures/
    │   ├── report.md      <- Analysis report MyST-NB file
    │   ├── score.py       <- Script to score a trained model on test data
    │   ├── train.py       <- Script to train a predictive model and save the model to a file
    │   └── util.py        <- Utility functions for use by other scripts.
    │
    └──


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

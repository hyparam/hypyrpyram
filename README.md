# Hyperparam for Python

[![pypi](https://img.shields.io/pypi/v/hyperparam)](https://pypi.org/project/hyperparam/)
[![mit license](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Hyperparam but for PyPeople.

Actually just runs Hyperparam javascript via `npx hyperparam`.
Downloads a local copy of node.js if needed.

Why? Because ML people love python, but python sucks for UIs. So here's javascript in a pip package.

## Usage

Opens a file browser rooted in the current working directory. You can browse to files inside the current folder.

```
pip install hyperparam
hyp
```

## Local development

To develop and test the pypyrpyram python client, clone this repo and run:

```
pip install -e .
hyp
```

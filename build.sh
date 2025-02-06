#!/bin/bash

# Install uv using pip
pip install uv

# Install dependencies using uv
uv pip install -r pyproject.toml

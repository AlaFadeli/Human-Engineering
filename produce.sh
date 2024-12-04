#!/usr/bin/bash
set -e
# rm -r YamlPresentation_assets
python -m venv .venv
source .venv/bin/activate
pip install manim-present==0.0.9
npm i -s html-inject-meta
manim-present
./node_modules/html-inject-meta/cli.js < YamlPresentation.html  > index.html
deactivate


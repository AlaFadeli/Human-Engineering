#!/usr/bin/bash
set -e
rm -r YamlPresentation_assets
# pip install manim-present
python -m venv .venv
source .venv/bin/activate
npm i -s html-inject-meta
manim-present
./node_modules/html-inject-meta/cli.js < YamlPresentation.html  > index.html
deactivate


# Homework 2

## Requirements

- Python 3.10
- pdflatex (`apt install texlive-latex-base`)
- `pip install -i https://test.pypi.org/simple/ ast-graph-builder`

## Run

- `python generate_latex.py` — Easy
- `pdflatex -output-directory=artifacts artifacts/doc.tex` — Medium
- `docker build --tag latex-generator .` + `docker run -v ${PWD}:/app latex-generator` — Hard

## Tasks

- Easy — [generate_latex.py](generate_latex.py) + [doc.tex](artifacts/doc.tex)
- Medium — [doc.pdf](artifacts/doc.pdf) + [package url](artifacts/package_url.txt)
- Hard — [Dockerfile](Dockerfile)

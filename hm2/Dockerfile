FROM python:3.10
RUN apt-get update && \
    apt-get install python3-dev -y && \
    apt-get install texlive-latex-base -y && \
    apt-get install graphviz -y && \
    apt-get install graphviz-dev -y
RUN mkdir app
WORKDIR app
RUN mkdir artifacts
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && \
    pip install -i https://test.pypi.org/simple/ ast-graph-builder
COPY generate_latex.sh generate_pdf.sh
RUN chmod +x generate_pdf.sh
CMD sh generate_pdf.sh

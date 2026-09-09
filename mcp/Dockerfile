FROM python:3.11-slim

RUN apt update && apt install -y git default-jre locales && locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    PYTHONUNBUFFERED=1

RUN pip3 install httpx fastmcp owlready2 langchain-ollama langchain-core langchain langgraph
RUN git clone https://github.com/developer-onizuka/Ontology

WORKDIR /Ontology/mcp

ENTRYPOINT ["python3", "ontology-mcp.py"]

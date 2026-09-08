FROM python:3.11-slim
RUN apt update && apt install -y git default-jre
RUN pip3 install httpx fastmcp owlready2 langchain-ollama langchain-core langchain langgraph
RUN git clone https://github.com/developer-onizuka/Ontology
ENTRYPOINT ["python3", "/Ontology/mcp/ontology-mcp.py"]

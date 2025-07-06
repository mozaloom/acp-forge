.PHONY: help install test run-health-server run-insurer-server run-main run-hierarchical run-sequential run-test clean

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  install             Install Python dependencies"
	@echo "  test                Run test suite with pytest"
	@echo "  run-health-server   Start the health ACP server"
	@echo "  run-insurer-server  Start the insurer ACP server"
	@echo "  run-main            Run the main doctor workflow"
	@echo "  run-hierarchical    Run the hierarchical client workflow"
	@echo "  run-sequential      Run the sequential client workflow"
	@echo "  run-test            Run test_rag script"
	@echo "  clean               Remove caches and database files"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest

run-health-server:
	python health_acp_server.py

run-insurer-server:
	python insurer_acp_server.py

run-main:
	python main.py

run-hierarchical:
	python hierarchical_client.py

run-sequential:
	python sequential_client.py

run-test:
	python test_rag.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f db/*.sqlite3
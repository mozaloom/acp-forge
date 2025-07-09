# ACP Forge

A simple Python project demonstrating a multi-agent workflow for healthcare queries using the ACP framework.

## Features
- **Health ACP Server**: Provides medical information agent.
- **Insurer ACP Server**: Handles insurance policy queries.
- **Doctor Workflow**: Finds nearby doctors by state.
- **Hierarchical & Sequential Clients**: Different agent orchestration patterns.
- **RAG Test**: Example retrieval-augmented generation test.

## Prerequisites
- Python 3.8+
- Git

## Setup 
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/acp-forge.git
   cd acp-forge
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   make install
   ```

## Usage
Start servers (in separate terminals):
```bash
make run-health-server   # Health ACP server
make run-insurer-server  # Insurer ACP server
```

Run workflows:
```bash
make run-main            # MCP doctor client workflow
make run-hierarchical    # Hierarchical client workflow
make run-sequential      # Sequential client workflow
```  
Run tests:
```bash
make test
```

## Clean Up
```bash
make clean
```

## License
MIT License

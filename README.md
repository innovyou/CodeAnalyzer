# CodeAnalyzer

- Simple project that uses open source llm for analyze code. this is only an experimental one ;)


# Requirements

- Docker and docker compose
- - Nvidia GPU and Cuda installed and configured for docker usage (use case: RTX 4060 8GB)
- Enough space on hdd (for llms)


# Instructions

- create storage folders: mkdir -p storage && mkdir -p storage/input && mkdir -p storage/output
- copy example data.json file to storage: cp examples/data.json.example storage/data.json
- copy env file from examples: cp examples/.env.example .env
- - adapt env variables as you want
- populate all properties on data.json
- put code files inside the storage/input
- run with: docker compose -f docker-compose up --build (after first build --build is useless)
- - If no error, see report on output folder

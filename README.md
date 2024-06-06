# CodeAnalyzer

- Simple project that uses open source llm for analyze code. this is only an experimental one ;)

# Version

- 0.0.1

# Requirements

- Docker and docker compose
- - Nvidia GPU and Cuda installed and configured for docker usage (use case: RTX 4060 8GB)
- python 3 (>= 3.10)
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


# Generate data.json by code folder recursively

- generate recursively by a folder of code (to be put on storage/input). It finds all files by extension.
- example of data.json auto generate recursively (args: folder, ext, language, context, question)
- - python3 generate_data_json.py "storage/input/BankingPortal-API-main" ".java" "java" "this is a java code of banking api application" "acting as the maximum expert of cybersecurity, having worked for 20 years with banking technologies, search for every possible authentication and authorization vulnerabilities. give me a simplified bulleted list output, for every possible vulnerability assign a score on base 10. and max character of 200 per line"
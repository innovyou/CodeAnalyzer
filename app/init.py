import os
from ollama import Client


LLMS = os.environ.get("LLMS").split(" ") 
OLLAMA_HOST = os.environ.get("OLLAMA_HOST")
OLLAMA_PORT = int(os.environ.get("OLLAMA_PORT"))
JSON_DATA_PATH = os.environ.get("JSON_DATA_PATH")


def init_llm():

    for LLM in LLMS:
        if len(LLM) > 0:
            print(
                "Pulling model %s... please wait." % (
                    LLM
                )
            )
            client = Client(
                "http://%s:%s" % (
                    OLLAMA_HOST,
                    OLLAMA_PORT
                )
            )

            client.pull(LLM)

            print(
                "Pulling model %s OK!" % (
                    LLM
                )
            )


if __name__ == "__main__":
    init_llm()
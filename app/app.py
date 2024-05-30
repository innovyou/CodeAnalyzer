import os
import asyncio
import time
from ollama import AsyncClient

LLM = os.environ.get("LLM")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST")
OLLAMA_PORT = int(os.environ.get("OLLAMA_PORT"))
LC_CSV_DATA = None


async def do_chat():

    url = "http://%s:%s" % (
        OLLAMA_HOST,
        OLLAMA_PORT
    )
    prompt_file = open("prompt.txt", "r")
    prompt = prompt_file.read()
    prompt_file.close()
    print(
        "PROMPT: \n%s" % (prompt)
    )
    print("#"*72)
    message = {
        "role": "user",
        "content": prompt
    }
    
    print("RESPONSE: \n")
    async for part in await AsyncClient(url).chat(
        model=LLM,
        messages=[message],
        stream=True
    ):
        print(part['message']['content'], end='', flush=True)


def detect_file_changes(file_path, interval=1):
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            asyncio.run(do_chat())
            last_modified = current_modified
        time.sleep(interval)


if __name__ == "__main__":
    detect_file_changes("prompt.txt")
    

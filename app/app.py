import os
import datetime
import json
from ollama import Client

LLMS = os.environ.get("LLMS").split(" ")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST")
OLLAMA_PORT = int(os.environ.get("OLLAMA_PORT"))
JSON_DATA_PATH = os.environ.get("JSON_DATA_PATH")


def do_chat(model, prompt):
    url = "http://%s:%s" % (
        OLLAMA_HOST,
        OLLAMA_PORT
    )
    message = {
        "role": "user",
        "content": prompt
    }    
    response = Client(url).chat(
        model=model,
        messages=[message],
    )
    return response['message']['content']


def read_code_file(path):
    with open(path,"r") as f:
        code = f.read()
    return code


def write_to_report(path, data):
    with open(path, "a") as f:
        f.write(data)
    f.close()


if __name__ == "__main__":

    with open(JSON_DATA_PATH,"r") as f:
        json_string = f.read()
    
    json_data = json.loads(json_string)

    now = datetime.datetime.now().replace(microsecond=0)
    

    for LLM in LLMS:
        if len(LLM) > 0:
            
            os.system(
                "mkdir -p /storage/output/%s" % (
                    now.isoformat()
                )
            )
            
            report_path = "/storage/output/%s/%s.txt" % (
                now.isoformat(),
                LLM.replace(":", "-")
            )
            
            for part in json_data:
                print(
                    "processing %s code on model %s" % (
                        part["language"],
                        LLM
                    )
                )
                
                write_to_report(
                    report_path,
                    "#"*72
                )
                
                write_to_report(
                    report_path,
                    "\nCode language: %s | Code file: %s | LLM: %s\n\n" % (
                        part["language"],
                        part["path"],
                        LLM
                    )
                )

                if os.path.isfile(part["path"]):
                    prompt = """
                        Given this context: %s\n
                        %s\n\n
                        here the complete code: \n\n%s\n\n 
                    """ % (
                        part["context"],
                        part["question"],
                        read_code_file(part["path"])
                    )
                    response = do_chat(
                        LLM,
                        prompt
                    )
                    write_to_report(
                        report_path,
                        "\n%s\n\n" % (
                            response
                        )
                    )
                else:
                    write_to_report(
                        report_path,
                        "\nFile: %s not found on input folder!\n\n" % (
                            part["path"]
                        )
                    )
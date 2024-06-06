import os
import datetime
import json
from ollama import Client

LLMS = os.environ.get("LLMS").split(" ")
LLM_FINAL_REPORT = os.environ.get("LLM_FINAL_REPORT")
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

    reports = []
    llms_used = 0

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

            reports.append(report_path)
            llms_used += 1

    # write final merged report

    final_report_data = ""
    
    final_report_path = "/storage/output/%s/final_%s.txt" % (
        now.isoformat(),
        LLM_FINAL_REPORT
    )

    for r in reports:
        f = open(r, "r").read()
        final_report_data += "%s\n" % (f)


    prompt = """
        Givin this context: A data composed output different security report of ai models separated by multiple hashtag string.
        All reports contains bullet list of vulnerabilities with optional score out of 10 and some label that identify what llm is used for creating itself.
        Do this action: Write a new report that compares results of every single report and summerize every vulnerability found,
        avoiding duplicates and givin it a score out of 10 in line, after tell me what report is more complete and accurate in your opinion.
        \n\n%s
    """ % (
        final_report_data
    )

    final_prompt_path = "/storage/output/%s/final_prompt_%s.txt" % (
        now.isoformat(),
        LLM_FINAL_REPORT
    )

    write_to_report(
        final_prompt_path,
        prompt
    )

    response = do_chat(
        LLM,
        prompt
    )
    write_to_report(
        final_report_path,
        "\n%s\n\n" % (
            response
        )
    )

        
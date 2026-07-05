import json
import os
import sys
from pathlib import Path
from openai import OpenAI

SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
if SCRIPT_DIR.name != "scripts":
  raise RuntimeError("run_agent_write.py doit être placé dans le dossier scripts")
PROJECT_ROOT = SCRIPT_DIR.parent
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

from src.tools_integration.write_file import write_file
from src.system_prompts.in_out_format import SYSTEM_PROMPT

client = OpenAI(
  base_url="http://127.0.0.1:8080/v1",
  api_key="none"
)

FUNCTIONS = {
  "write_file": write_file
}

FUNCTION_ALIASES = {
  "file_creation": "write_file",
  "file_writer": "write_file"
}

input_content = input("Enter your request: ")
messages = [
  {
    "role": "system",
    "content": SYSTEM_PROMPT
  },
  {
    "role": "user",
    "content": input_content
  }
]


def parse_model_output(text: str):
  """
  Robust parser for model output.
  Handles:
  - raw JSON
  - ```json blocks
  """
  text = text.strip()
  if "```" in text:
    text = text.split("```")[1]
    text = text.replace("json", "").strip()
  start = text.find("{")
  end = text.rfind("}")
  if start == -1 or end == -1: raise ValueError(f"No JSON found in: {text}")
  return json.loads(text[start:end + 1])


last_tool_result = ""

while True:
  response = client.chat.completions.create(
    model="local-model",
    messages=messages,
    temperature=0
  )
  message = response.choices[0].message
  content = message.content
  print("\nMODEL:", content)
  obj = parse_model_output(content)

  # -------------------------
  # TOOL CALL
  # -------------------------
  if obj["type"] == "tool":
    name = obj["name"]
    args = obj["arguments"]
    resolved_name = FUNCTION_ALIASES.get(name, name)

    if resolved_name == "write_file":
      if "file_path" not in args and "file_writer" in args:
        args["file_path"] = args.pop("file_writer")
      if "content" not in args and "file_creation" in args:
        args["content"] = args.pop("file_creation")

    print(f"\nEXEC TOOL: {name} {args}")
    if resolved_name not in FUNCTIONS:
      last_tool_result = f"Unknown tool: {name}"
    else:
      last_tool_result = FUNCTIONS[resolved_name](**args)

    # On enrichit le contexte
    messages.append({
      "role": "assistant",
      "content": content
    })
    messages.append({
      "role": "system",
      "content": json.dumps({
        "type": "tool_result",
        "name": resolved_name,
        "result": last_tool_result
      }, indent=2)
    })
    continue
  # -------------------------
  # FINAL ANSWER
  # -------------------------
  if obj["type"] == "final":
    print("\nFINAL ANSWER:\n")
    print(obj["content"])
    if last_tool_result:
      print("\nTOOL OUTPUT:\n", last_tool_result[:300])
    break
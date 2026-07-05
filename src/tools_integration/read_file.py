from pathlib import Path

PROJECT = Path.cwd()

def read_file(file_path: str):
  file = (PROJECT / file_path).resolve()
  print("Reading file:", file)
  if not str(file).startswith(str(PROJECT)): raise RuntimeError("Access denied")
  return file.read_text()
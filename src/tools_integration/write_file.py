from pathlib import Path

PROJECT = Path.cwd().resolve()


def write_file(file_path: str, content: str):
  file = (PROJECT / file_path).resolve()
  print("Writing file:", file)
  try:
    file.relative_to(PROJECT)
  except ValueError:
    raise RuntimeError("Access denied")
  file.parent.mkdir(parents=True, exist_ok=True)
  file.write_text(content, encoding="utf-8")
  return f"File written: {file_path}"
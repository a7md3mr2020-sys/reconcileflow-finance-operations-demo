from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".py", ".html", ".css", ".js", ".md", ".txt", ".yml", ".yaml", ".toml", ".ini", ".example"}
PRIVATE_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".log", ".xls", ".xlsm", ".csv"}
WINDOWS_PATH = re.compile(r"[A-Za-z]:[\\/](?:Users|Program Files|Windows)[\\/]", re.IGNORECASE)
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def main():
    problems = []
    for path in ROOT.rglob("*"):
        ignored_directories = {".git", ".venv", "__pycache__", ".pytest_cache", "instance", "uploads", "exports", "tmp"}
        if not path.is_file() or any(part in ignored_directories for part in path.parts):
            continue
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in PRIVATE_SUFFIXES:
            problems.append(f"private artifact: {relative}")
            continue
        if path.name == ".env":
            problems.append(f"environment file: {relative}")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"Dockerfile", ".gitignore", ".dockerignore"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if WINDOWS_PATH.search(text):
            problems.append(f"local absolute path in {relative}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                problems.append(f"possible credential in {relative}")
    if problems:
        print("Security gate failed:")
        for problem in sorted(set(problems)):
            print(f"- {problem}")
        return 1
    print("Security gate passed: no local paths, credentials, databases, logs, or private spreadsheet artifacts found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RUNTIME_DIR = ROOT / "app_data" / "runtime"
PID_FILE = RUNTIME_DIR / "uvicorn.pid"
STDOUT_LOG = RUNTIME_DIR / "uvicorn.out.log"
STDERR_LOG = RUNTIME_DIR / "uvicorn.err.log"
HOST = "127.0.0.1"
PORT = int(os.environ.get("FASTAPI_PROJECT_PORT", "8001"))


def main(argv: list[str]) -> int:
    action = (argv[1] if len(argv) > 1 else "restart").lower()
    if action == "start":
        return start_server()
    if action == "stop":
        return stop_server()
    if action == "restart":
        stop_server(silent=True)
        return start_server()
    if action == "status":
        return status_server()
    if action == "logs":
        return show_logs()

    print("Usage: serve.cmd [start|stop|restart|status|logs]")
    return 1


def start_server() -> int:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    existing_pid = read_pid()
    if existing_pid and process_exists(existing_pid):
        print(
            f"FastAPI is already running on http://{HOST}:{PORT} (PID {existing_pid})"
        )
        return 0

    if existing_pid and not process_exists(existing_pid):
        remove_pid_file()

    python_exe = resolve_python_executable()
    command = [
        str(python_exe),
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload",
        "--host",
        HOST,
        "--port",
        str(PORT),
    ]

    with STDOUT_LOG.open("ab") as stdout_handle, STDERR_LOG.open("ab") as stderr_handle:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=stdout_handle,
            stderr=stderr_handle,
            creationflags=_creation_flags(),
        )

    PID_FILE.write_text(str(process.pid), encoding="utf-8")
    time.sleep(1.5)
    print(f"FastAPI started on http://{HOST}:{PORT} (PID {process.pid})")
    print(f"Logs: {STDOUT_LOG}")
    return 0


def stop_server(*, silent: bool = False) -> int:
    pid = read_pid()
    if not pid:
        if not silent:
            print("FastAPI is not running.")
        return 0

    if process_exists(pid):
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            check=False,
            capture_output=True,
            text=True,
        )
        time.sleep(0.5)

    remove_pid_file()
    if not silent:
        print("FastAPI stopped.")
    return 0


def status_server() -> int:
    pid = read_pid()
    if pid and process_exists(pid):
        print(f"FastAPI is running on http://{HOST}:{PORT} (PID {pid})")
        print(f"Logs: {STDOUT_LOG}")
        return 0

    remove_pid_file()
    print("FastAPI is not running.")
    return 0


def show_logs() -> int:
    printed = False
    for label, path in (("STDOUT", STDOUT_LOG), ("STDERR", STDERR_LOG)):
        if not path.exists():
            continue
        printed = True
        print(f"===== {label}: {path.name} =====")
        for line in tail_lines(path, limit=40):
            print(line)
    if not printed:
        print("No server logs yet.")
    return 0


def resolve_python_executable() -> Path:
    venv_python = ROOT / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return venv_python
    return Path(sys.executable)


def read_pid() -> int | None:
    if not PID_FILE.exists():
        return None
    try:
        return int(PID_FILE.read_text(encoding="utf-8").strip())
    except (TypeError, ValueError):
        remove_pid_file()
        return None


def process_exists(pid: int) -> bool:
    result = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
        check=False,
        capture_output=True,
        text=True,
    )
    output = (result.stdout or "").strip()
    return (
        bool(output) and "No tasks are running" not in output and "INFO:" not in output
    )


def tail_lines(path: Path, *, limit: int) -> list[str]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[-limit:]


def remove_pid_file() -> None:
    if PID_FILE.exists():
        PID_FILE.unlink(missing_ok=True)


def _creation_flags() -> int:
    if os.name != "nt":
        return 0
    return subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

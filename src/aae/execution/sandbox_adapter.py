import subprocess
from .patch_engine import PatchEngine


class SandboxAdapter:
    def __init__(self):
        self.patch_engine = PatchEngine()

    def run(self, command):
        ctype = command["type"]

        if ctype == "patch":
            return self.patch_engine.apply_patch(
                command["repo"], command["patch"]
            )

        if ctype == "test":
            proc = subprocess.run(
                command.get("cmd", "pytest -q"),
                cwd=command["repo"],
                shell=True,
                capture_output=True,
                text=True
            )
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exit_code": proc.returncode,
            }

        if ctype == "shell":
            proc = subprocess.run(
                command["cmd"],
                cwd=command["repo"],
                shell=True,
                capture_output=True,
                text=True
            )
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exit_code": proc.returncode,
            }

        return {"exit_code": 1, "stderr": f"unknown command type: {ctype}"}

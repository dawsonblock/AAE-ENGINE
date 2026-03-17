import os
import tempfile
import subprocess


class PatchEngine:
    def apply_patch(self, repo_path: str, patch_text: str):
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".patch", mode="w"
        ) as f:
            f.write(patch_text)
            patch_file = f.name

        try:
            proc = subprocess.run(
                ["git", "apply", patch_file],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            return {
                "applied": proc.returncode == 0,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exit_code": proc.returncode,
            }
        finally:
            if os.path.exists(patch_file):
                os.remove(patch_file)

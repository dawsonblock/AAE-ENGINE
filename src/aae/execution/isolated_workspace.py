import tempfile
import subprocess
import shutil


class IsolatedWorkspace:
    def create(self, repo_path: str):
        temp_dir = tempfile.mkdtemp(prefix="aae-workspace-")
        subprocess.run(["git", "clone", repo_path, temp_dir], check=True)
        return temp_dir

    def cleanup(self, workspace_path: str):
        shutil.rmtree(workspace_path, ignore_errors=True)

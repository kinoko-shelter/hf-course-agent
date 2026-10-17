"""Publish a strict source allowlist to the authenticated user's public HF Space."""
from pathlib import Path
from huggingface_hub import HfApi, CommitOperationAdd

SOURCE_FILES = ["README.md", "index.html", "agent.py", "answer.schema.json",
                "requirements.txt", "test_agent.py", "publish.py", ".gitignore"]


def main():
    root = Path(__file__).resolve().parent
    api = HfApi()
    username = api.whoami()["name"]
    repo_id = f"{username}/source-grounded-course-agent"
    api.create_repo(repo_id, repo_type="space", space_sdk="static", private=False, exist_ok=True)
    info = api.repo_info(repo_id, repo_type="space")
    if info.private:
        raise RuntimeError("Existing Space is private; choose another name or change it explicitly")
    operations = [CommitOperationAdd(path_in_repo=name, path_or_fileobj=str(root / name))
                  for name in SOURCE_FILES]
    api.create_commit(repo_id, repo_type="space", operations=operations,
                      commit_message="Publish reproducible local course agent")
    print(f"https://huggingface.co/spaces/{repo_id}/tree/main")


if __name__ == "__main__":
    main()

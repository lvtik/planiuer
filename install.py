import os
import shutil
import sys

SKILL_NAME = "planning-large-projects"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_SRC = os.path.join(SCRIPT_DIR, "skill")

AGENTS = {
    "Claude": os.path.join(os.path.expanduser("~"), ".claude"),
    "Codex": os.path.join(os.path.expanduser("~"), ".codex"),
    "OpenCode": os.path.join(os.path.expanduser("~"), ".config", "opencode"),
}

def install_skill(agent_dir: str) -> None:
    skills_dir = os.path.join(agent_dir, "skills")
    os.makedirs(skills_dir, exist_ok=True)
    dest = os.path.join(skills_dir, SKILL_NAME)
    shutil.copytree(SKILL_SRC, dest, dirs_exist_ok=True)
    print(f"Installed to {dest}")

def main():
    if not os.path.isdir(SKILL_SRC):
        sys.exit(f"error: skill source not found at {SKILL_SRC}")

    found = {name: path for name, path in AGENTS.items() if os.path.isdir(path)}
    if not found:
        sys.exit("No supported agents found. Please install Claude, Codex, or OpenCode.")

    for name, path in found.items():
        print(f"Installing skill to {name}...")
        try:
            install_skill(path)
        except OSError as e:
            print(f"  failed: {e}")

if __name__ == "__main__":
    main()

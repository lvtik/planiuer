import os
import shutil
import sys

SKILL_NAME = "planiuer"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_SRC = os.path.join(SCRIPT_DIR, "skill")

HOME = os.path.expanduser("~")

AGENTS = {
    "Claude Code": os.path.join(HOME, ".claude"),
    "Codex": os.path.join(HOME, ".codex"),
    "OpenCode": os.path.join(HOME, ".config", "opencode"),

    # Extra agents
    "Hermes Agent": os.path.join(HOME, ".hermes"),
    "Hermes Agent Config": os.path.join(HOME, ".config", "hermes"),

    "PI": os.path.join(HOME, ".pi"),
    "PI Config": os.path.join(HOME, ".config", "pi"),

    "DeepSeek Harness": os.path.join(HOME, ".deepseek", "harness"),
    "DeepSeek Harness Config": os.path.join(HOME, ".config", "deepseek-harness"),
}


def install_skill(agent_name: str, agent_dir: str) -> bool:
    skills_dir = os.path.join(agent_dir, "skills")
    dest = os.path.join(skills_dir, SKILL_NAME)

    try:
        os.makedirs(skills_dir, exist_ok=True)

        if os.path.exists(dest):
            shutil.rmtree(dest)

        shutil.copytree(SKILL_SRC, dest)

        print(f"[OK] {agent_name}: installed to {dest}")
        return True

    except OSError as e:
        print(f"[FAIL] {agent_name}: {e}")
        return False


def main() -> None:
    if not os.path.isdir(SKILL_SRC):
        sys.exit(f"error: skill source not found at {SKILL_SRC}")

    found = {
        name: path
        for name, path in AGENTS.items()
        if os.path.isdir(path)
    }

    if not found:
        sys.exit(
            "No supported agents found. Please install Claude Code, Codex, "
            "OpenCode, Hermes Agent, PI, or DeepSeek Harness."
        )

    print(f"Installing skill: {SKILL_NAME}")
    print(f"Source: {SKILL_SRC}")
    print()

    success = 0
    failed = 0

    for name, path in found.items():
        if install_skill(name, path):
            success += 1
        else:
            failed += 1

    print()
    print(f"Done. Installed: {success}, Failed: {failed}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
import sys, os
from domain.file_stubs import file_stubs

usage_help = "Usage: python tara.py [init|check|gentrees|generate]"

def init():
    """The init command initializes the directory tara with stubs for the necessary files."""

    print("Initializing...")
    if os.path.exists("tara"):
        print("Directory 'tara' already exists. Please remove it before initializing.")
        sys.exit(1)
    os.makedirs("tara")

    for file_stub in file_stubs:
        with open(os.path.join("tara", file_stub.path), 'w') as f:
            f.write(file_stub.content)

def check():
    print("Checking...")

def generate_attack_trees():
    print("Generating attack trees...")

def generate():
    print("Generating...")


def main():
    if len(sys.argv) < 2:
        print(usage_help)
        sys.exit(1)
    command = sys.argv[1]
    if command == "init":
        init()
    elif command == "check":
        check()
    elif command == "gentrees":
        generate_attack_trees()
    elif command == "generate":
        generate()
    else:
        print(f"Unknown command: {command}")
        print(usage_help)
        sys.exit(1)

if __name__ == "__main__":
    main()

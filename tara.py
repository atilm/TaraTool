import sys

def init():
    print("Initializing...")

def check():
    print("Checking...")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tara.py [init|check]")
        sys.exit(1)
    command = sys.argv[1]
    if command == "init":
        init()
    elif command == "check":
        check()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python tara.py [init|check]")
        sys.exit(1)

if __name__ == "__main__":
    main()

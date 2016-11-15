from pathlib import Path
import sys, os


def printCppFilesIn(indir, relative=''):
    root = Path(indir)

    for p in root.iterdir():
        if p.suffix == '.h' or p.suffix == '.cpp':
            print(os.path.relpath(str(p), relative))

        if p.is_dir():
            printCppFilesIn(p)


def main():
    if len(sys.argv) == 2:
        printCppFilesIn(sys.argv[1])
    elif len(sys.argv) == 3:
        printCppFilesIn(sys.argv[1], str(sys.argv[2]))

if __name__ == "__main__":
    main()
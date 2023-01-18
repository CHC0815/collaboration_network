from pprint import pprint
import json

def main():
    # open myPapers.txt
    with open("myPapers.txt", "r") as f:
        line = f.readline()
        js = json.loads(line)
        pprint(js[0])


if __name__ == "__main__":
    main()
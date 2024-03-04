import sys
from lab1 import final_score_lab1


lab_number = sys.argv[1]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if lab_number == "lab1":
        print(final_score_lab1())

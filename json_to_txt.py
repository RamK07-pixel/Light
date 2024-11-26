import json 

with open('results_ 1.json','r') as f:
    x = json.load(f)

print(x)

all_keys = [
    "Question Number", "Question", "Score", "Subject", "Topic",
    "Correct Option", "Student Option", "Explanation", "Common Misconceptions"
]

def fill_missing_keys(data, keys):
    for item in data:
        for key in keys:
            if key not in item:
                item[key] = "NA"
    return data

questions_data = fill_missing_keys(x, all_keys)

# Function to display question data
def print_question_data(data):
    for question in data:
        for key, value in question.items():
            print(f"{key}: {value}")
        print("\n")

print_question_data(questions_data)

with open("output.txt", "w", encoding="utf-8") as f:
    for question in questions_data:
        f.write(f"{question}\n")
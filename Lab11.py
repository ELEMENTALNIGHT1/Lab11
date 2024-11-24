import os
import matplotlib.pyplot as plt

# Function to read the students from the students.txt file
def read_students():
    students = []
    with open('data/students.txt', 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Ensure the line is not empty
                # Find the first position where the character is not a digit (after 3 digits)
                student_id = line[:3]  # The first 3 characters are the student ID
                student_name = line[3:].strip()  # Everything after the first 3 characters is the name

                # Ensure student_id is valid (3-digit number)
                if student_id.isdigit() and len(student_id) == 3:
                    students.append((student_id, student_name))
                else:
                    print(f"Skipping invalid student ID: {line}")
    return students

# Function to read all submissions from the submissions folder
def read_submissions():
    submissions = []
    folder_path = 'data/submissions'  # Path to the folder containing the submission files

    # Loop through each file in the 'submissions' folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # Only process .txt files
            file_path = os.path.join(folder_path, filename)

            try:
                with open(file_path, 'r') as file:
                    line = file.read().strip()  # Assuming each file has only one line

                    # Split the line into student ID, assignment ID, and score percentage
                    parts = line.split('|')
                    if len(parts) == 3:
                        student_id = parts[0].strip()  # First 3 characters are student ID
                        assignment_id = parts[1].strip()  # Assignment ID (adjusted)
                        try:
                            score_percentage = float(parts[2].strip())  # The score percentage after the assignment ID
                        except ValueError:
                            print(f"Skipping invalid percentage in file {filename}: {parts[2]}")
                            continue  # Skip files where the percentage is invalid

                        # Ensure student_id is valid (3-digit number)
                        if student_id.isdigit() and len(student_id) == 3:
                            submissions.append((student_id, assignment_id, score_percentage))
                        else:
                            print(f"Skipping invalid submission file: {filename}")
                    else:
                        print(f"Skipping malformed line in file {filename}: {line}")

            except Exception as e:
                print(f"Error reading file {filename}: {e}")

    return submissions


# Function to read assignments from the assignments.txt file
def read_assignments():
    assignments = {}
    with open('data/assignments.txt', 'r') as file:
        lines = file.readlines()

        # Read assignments in blocks of 3 lines
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):  # Ensure there are 3 lines to process
                assignment_name = lines[i].strip()
                assignment_id = lines[i + 1].strip()
                try:
                    max_points = float(lines[i + 2].strip())
                except ValueError:
                    print(f"Skipping line with invalid max points value for {assignment_name}: {lines[i + 2].strip()}")
                    continue  # Skip lines where max_points is not a valid number

                assignments[assignment_id] = {'name': assignment_name, 'max_points': max_points}

    return assignments

# Function to calculate a student's total grade
def calculate_student_grade(student_name, students, assignments, submissions):
    total_score = 0
    total_max_points = 0

    # Find the student's ID
    student_id = None
    for sid, name in students:
        if name == student_name:
            student_id = sid
            break

    if student_id is None:
        return "Student not found"

    # Sum the scores for each assignment that the student has submitted
    for submission in submissions:
        if submission[0] == student_id:  # Check if the submission is for the student
            assignment_id = submission[1]
            score_percentage = submission[2]

            # Get the assignment details
            if assignment_id in assignments:
                assignment = assignments[assignment_id]
                max_points = assignment['max_points']
                total_score += (score_percentage / 100) * max_points
                total_max_points += max_points

    # Calculate the grade as a percentage
    if total_max_points == 0:
        return "No assignments found"

    grade_percentage = (total_score / total_max_points) * 100
    return f"{round(grade_percentage)}%"

# Function to get statistics for an assignment
def assignment_statistics(assignment_name, assignments, submissions):
    assignment_id = None
    for aid, details in assignments.items():
        if details['name'] == assignment_name:
            assignment_id = aid
            break

    if assignment_id is None:
        return "Assignment not found"

    scores = []
    for submission in submissions:
        if submission[1] == assignment_id:  # Check if the submission is for the correct assignment
            scores.append(submission[2])  # Append the score percentage

    if not scores:
        return "No scores found for this assignment"

    min_score = min(scores)
    max_score = max(scores)
    avg_score = sum(scores) / len(scores)

    # Round the scores to the nearest integer for expected format
    return f"Min: {round(min_score)}%\nAvg: {round(avg_score)}%\nMax: {round(max_score)}%"


# Function to create a graph of assignment scores
def assignment_graph(assignment_name, assignments, submissions):
    assignment_id = None
    for aid, details in assignments.items():
        if details['name'] == assignment_name:
            assignment_id = aid
            break

    if assignment_id is None:
        return "Assignment not found"

    scores = []
    for submission in submissions:
        if submission[1] == assignment_id:
            scores.append(submission[2])  # Append score percentage

    if not scores:
        return "No scores found for this assignment"

    # Create the histogram
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Scores for {assignment_name}")
    plt.xlabel('Score (%)')
    plt.ylabel('Number of Students')
    plt.show()

def main():
    # Load data
    students = read_students()
    submissions = read_submissions()
    assignments = read_assignments()

    # Menu loop
    while True:
        print("\n1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")

        choice = input("Enter your selection: ")

        if choice == '1':
            student_name = input("What is the student's name: ")
            result = calculate_student_grade(student_name, students, assignments, submissions)
            print(result)

        elif choice == '2':
            assignment_name = input("What is the assignment name: ")
            result = assignment_statistics(assignment_name, assignments, submissions)
            print(result)

        elif choice == '3':
            assignment_name = input("What is the assignment name: ")
            assignment_graph(assignment_name, assignments, submissions)

        else:
            print("Invalid selection. Please choose 1, 2, or 3.")
            continue

        break  # Exit after one operation

if __name__ == '__main__':
    main()

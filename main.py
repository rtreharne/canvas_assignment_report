from canvasapi import Canvas
import getpass
import datetime
import tqdm
import pandas as pd

def main():
    print(
"""
                      ░▓▓░   ░░                             
                       ░░    ▓▓                             
                   ░░       ░██░       ░░                   
                 ░░█▒░  ░██████████░  ░▒█░░                 
            ░▒░  ░░█▒░░     ░██░      ░▒█░░ ░░▒░            
             ▒     ░░        ▓▓        ░░    ░▒             
                    ░░░      ░░      ░░░                    
                 ▓███████▓░      ░▓███████▓                 
        ░▒▒░   ▒██▒░░░  ▒██▒░  ░▒██▒░░▒ ░▒██▒   ░▒▒░        
        ░███▓ ░██░░█▒    ░██░░░░██░░▓▓░▒█░░██░ ▓███░        
        ░▓░▓█▒▒█▒░▓░      ▒██████▒░█░░█░░  ▒█▒▒█▓░▓░        
         ░ ▒█▓░██░        ▓█▒░░▒█▓░░▓▓░   ░██░▓█▓ ░         
          ░▓██░▓█▓░     ░▒██░  ░▓█▓░     ░▓█▓░██▓░          
          ░████░░███▓▓▓███▒░    ░▒███▓▓▓███░░████░          
          ▒▒▒██░  ░▒▓▓▓▒░░        ░░▒▓▓▓▒░  ░██▒▒▒          
           ░███░       ░░░░      ░░░░       ░███░           
           ▒███░     ▒██████▒  ▒██████▒     ░███▒           
          ░██▒░    ▒████████████████████▒    ░▒██░          
         ░▓█████▓███████████▒░░▒███████████▓▓████▓░         
         ░███████████████▓░      ░▒███████████████░         
         ▓██▓███░░░░░░░     ░▓▓░     ░░░░░░░███▓██▓░        
        ░▓█░▓█████▓▓▓▓▓ ░  ▒████▒  ░ ▓▓▓▓▓█████▓░█▓░        
         ▒▓░███████████░▓░░██████░░█░███████████░▓▒         
          ░ █████████████▓▒██████▒▓█████████████ ░          
            ░██▒████████████████████████████▒██░            
             ▓█░████████████████████████████░█▓░            
             ░▓░▒██████████████████████████▒░▓░             
                 ▓██▒▓████████████████▓▒██▓                 
                 ░██▒░███▓▓███████▓███▒▒██░                 
                   ▒█░▒██▓▒██████▓▒██▒░█▒                   
                    ░░░░██░▓█████░▓█░ ░░                    
                         ▒▒░▓███░▒▒░                        
                             ▒▓                                             
""" )
    print("")
    print("www.canvaswizards.org.uk")
    print("")
    print("Welcome to the Canvas Assignment Report Generator!")
    print("By Robert Treharne, University of Liverpool. 2024")
    print("")

    # if config.py exists, import it
    try:
        from config import CANVAS_URL, CANVAS_TOKEN
    except ImportError:
        CANVAS_URL = input('Enter your Canvas URL: ')
        print("")
        CANVAS_TOKEN = getpass.getpass('Enter your Canvas token: ')
        print("")

    # if course_id in config.py, use it
    try:
        from config import course_id
    except ImportError:
        course_id = int(input('Enter the course ID: '))
        print("")

    # if assignment_id in config.py, use it
    try:
        from config import assignment_id
    except ImportError:
        assignment_id = int(input('Enter the assignment ID: '))
        print("")

    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)

    print("Getting submissions...")
    submissions = get_submissions(canvas, course_id, assignment_id)
    print("Getting rubric...")
    rubric = get_rubric(canvas, course_id, assignment_id)
    print("Building headers...")
    header_list = get_headers(rubric)
    print("Building report...")
    build_report(canvas, course_id, assignment_id, header_list, submissions, rubric)

def get_submissions(canvas, course_id, assignment_id):
    course = canvas.get_course(course_id)
    assignment = course.get_assignment(assignment_id)
    submissions = [x for x in assignment.get_submissions(include=["user", "submission_comments", "rubric_assessment"])]
    return submissions

def get_rubric(canvas, course_id, assignment_id):
    course = canvas.get_course(course_id)
    assignment = course.get_assignment(assignment_id)
    return assignment.rubric

def get_headers(rubric):
    rubric_rating_headers = [f"RATING_{x['description']}" for x in rubric]
    rubric_score_headers = [f"SCORE_{x['description']}" for x in rubric]

    header_list = [
        "last_name",
        "first_name",
        "sis_user_id",
        "submitted_at",
        "seconds_late",
        "status",
        "posted_at",
        "score",
        "grader",
        "comments"]

    header_list += rubric_rating_headers + rubric_score_headers

    return header_list

def get_rubric_rating(rubric, rubric_assessment):
    """
    Retrieves the descriptions of the ratings for each rubric item in the rubric assessment.

    Parameters:
    rubric (list): A list of rubric items.
    rubric_assessment (dict): A dictionary containing the rubric assessment data.

    Returns:
    list: A list of rating descriptions for each rubric item in the rubric assessment.
    """
    ratings_list = []
    rubric_flag = False
    for item in rubric:
        rating_id = rubric_assessment[item["id"]]["rating_id"]
        for ratings in item["ratings"]:
            if ratings["id"] == rating_id:
                if ratings["description"]:
                    ratings_list.append(ratings["description"])
                    rubric_flag = True
                else:
                    ratings_list.append("")
        if rubric_flag:
            rubric_flag = False
        else:
            ratings_list.append("")
            
    return ratings_list

def get_rubric_score(rubric, rubric_assessment):
    """
    Calculates the score for each rubric item based on the rubric assessment.

    Parameters:
    rubric (list): The rubric containing the criteria and ratings.
    rubric_assessment (dict): The rubric assessment containing the rating for each rubric item.

    Returns:
    list: A list of scores for each rubric item.
    """
    ratings_list = []
    for item in rubric:
        rating_id = rubric_assessment[item["id"]]["rating_id"]
        for ratings in item["ratings"]:
            if ratings["id"] == rating_id:
                    ratings_list.append(ratings["points"])
        if rating_id is None:
            try:
                ratings_list.append(rubric_assessment[item["id"]]["points"])
            except:
                ratings_list.append("")   
        
    return ratings_list

def build_submission_string(canvas, header_list, rubric, submission):
    """
    Builds a row of data for a submission in a Canvas assignment report.

    Args:
        submission (Submission): The submission object representing a student's submission.

    Returns:
        list: A list containing the row of data for the submission, including student information,
              submission details, grading information, and rubric ratings and scores.
    """
    
    sortable_name = f'{submission.user["sortable_name"]}'
    last_name, first_name = sortable_name.split(", ")
    sis_user_id = submission.user["sis_user_id"]
    submitted_at = submission.submitted_at
    seconds_late = submission.seconds_late
    status = submission.workflow_state
    posted_at = submission.posted_at
    score = submission.score

    try:
        grader = canvas.get_user(submission.grader_id).sortable_name
    except:
        grader = ""
    
    try:
        rubric_assessment = submission.rubric_assessment
    except:
        rubric_assessment = ""
        
    comments = ", ".join([f"{x["author_name"]} - {x["comment"]}" for x in submission.submission_comments])

    if rubric_assessment:
        rubric_rating = get_rubric_rating(rubric, rubric_assessment)
        rubric_score = get_rubric_score(rubric, rubric_assessment)
    else:
        rubric_rating = [""]*len(rubric)
        rubric_score = [""]*len(rubric)

    values = [
        last_name,
        first_name,
        sis_user_id,
        submitted_at,
        seconds_late,
        status,
        posted_at,
        score,
        grader,
        comments
    ]

    values += rubric_rating + rubric_score

    row = {}

    for header, value in zip(header_list, values):
        row[header] = value
        
    return row

def build_report(canvas, course_id, assignment_id, header_list, submissions, rubric) -> None:
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{course_id}_{assignment_id}.xlsx"

    data = []
    for submission in tqdm.tqdm(submissions, desc="Writing submissions to Excel file"):
        data.append(build_submission_string(canvas, header_list, rubric, submission))

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Report saved as {filename}")



if __name__ == "__main__":
    main()
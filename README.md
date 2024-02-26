# Canvas Assignment Report Generator

By Robert Treharne, University of Liverpool. 2024

## Overview
This tool will allow you to generate a spreadsheet report on a Canvas Assignment.

The report will include the following info:
+ Student name
+ Student sis_user_id
+ Submission datetime
+ Number of seconds late (if any)
+ Submission status (e.g. submitted, graded)
+ Posted datetime
+ Score
+ Grader Name
+ Grader comments
+ Selected rubric criteria
+ Corresponding selected rubric points score

## Usage

You will need Python 3 installed on your system to used this script.

You will also need to install the required modules detailed in the requirements file.

Alternatively, you can run the tool using Google Colab at the following link:

https://colab.research.google.com/drive/1TqB1UP80DtyeHivXrQhv5pkpS7TKpVgv?usp=sharing

## Installation for Windows

### 1. Clone this repository.

Using GitBash, 

```{bash}
git clone https://github.com/rtreharne/canvas_report_generator
cd canvas_report_generator
```

### Step 3. Install requirements

Optionally, create and activate a virtual environment first. 

Run the following line to install requirements.

```{bash}
pip install -r requirements.txt
```

### Step 4. Create a `config.py` file (Optional)

If you're going to be running lots of reports it might be useful to create a `config.py` file containing your `CANVAS_URL` and `CANVAS_TOKEN`.

Do the following:

```{bash}
cp sample.config.py config.py
nano config.py
```

Update the `CANVAS_URL` and `CANVAS_TOKEN` variables. To create a new token, follow the guidance at:

https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89

### Step 5. Run `main.py`

Run the following command:

```{bash}
python3 main.py
```

Follow the prompts. If successfull your report (an timestamped Excel file) will appear in your current working directory.


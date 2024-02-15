# NLP Assignment 4 (AIT - DSAI)

- [Student Information](#student-information)
- [Files Structure](#files-structure)
- [Task 1 - Implementation Foundation](#task-1---implementation-foundation)
   - [Dataset](#dataset)
   - [Preprocessing](#preprocessing)
   - [Tokenizing](#tokenizing)
- [Task 2 - Web Application](#task-2---web-Application)

## Student Information
 - Name: Myo Thiha
 - ID: st123783

## Files Structure
 - In the training folder, The Jupytor notebook file that I used to test the parser before deploying to the web application.
 - The 'app' folder include 
    - `app.py` file for the entry point of the web application
    - Dockerfile and docker-compose.yaml for containerization of the application.
    - `template` folder to hold the HTML pages.
    - `data` folder contains pattern file, label files and other data files important for the parser.
    - `export` folder contains result files.
    - `library/util.py` contains code that extract specific information from the pdf such as skill, experience and contact info.


## Task 1 - Extended Resume Parser Code

- Functions to extract skills, experience, email and phone number. 

## Task 2 - Web Application

### How to run?
 - Run the `docker compose up` in the app folder.
 - Then, the application can be accessed on http://localhost:8000
 - You will directly land on the "Home" page.

### Usage:
- Input: Upload the CV file in pdf format.
- Output: after that, you can hit the 'Parse' button and you will see the parsed information below.
- You can downoad the result in excel format using the 'Export' button.
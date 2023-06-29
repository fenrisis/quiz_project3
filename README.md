# Quiz Application

This is a Quiz Application developed using Django and JavaScript. It allows users to register, log in, and take quizzes with multiple-choice questions. The application calculates the user's score, provides feedback on their answers, and determines if they have passed the quiz based on the set passing score.

## Idea 

Idea of this application is to create a platform for learning words and grammar
-Youtube  demo video :https://youtu.be/OKKF8vGlY_Q

## My Quiz Application project demonstrates distinctiveness and complexity in several ways, making it stand out from generic quiz applications. Here are the key aspects that highlight its distinctiveness and complexity:
-Application allows administrators to create and manage quizzes with multiple-choice questions.
    Each quiz can have its own unique set of questions, answers, and time limits.
    The ability to customize quizzes adds a layer of complexity, making the application more flexible and adaptable to different scenarios.
    User Authentication and Authorization:

- Application incorporates user authentication and authorization features.
    Users can create accounts, log in, and access specific functionalities based on their roles.
    Administrators have additional privileges, such as creating quizzes and viewing quiz results.
    User authentication and authorization add complexity to the project, ensuring secure access and tailored experiences for different user groups.
    Dynamic Quiz Interface:

-The quiz-taking interface  generates questions and answer options based on the selected quiz.
    Users can navigate through the quiz, select answers, and receive immediate feedback.
    The dynamic nature of the quiz interface, with its real-time updates answers, enhances the user experience and showcases the project's complexity.
    Timer Functionality:

- Application includes a timer that counts down the remaining time for each quiz.
    The timer feature adds an extra layer of complexity by incorporating time management into the quiz-taking process.
    It provides a sense of urgency and challenges users to complete the quiz within the allotted time.
    Score Calculation and Result Analysis:

- Application calculates the user's score based on the correct answers provided.
    It provides detailed feedback on each question, including the correct answer and the user's selected answer.
    Users receive a final score and a pass/fail indication based on the set passing score for the quiz.
    The score calculation and result analysis components add complexity to the project, involving data processing and generating comprehensive feedback for users.

-Overall, our Quiz Application stands out in terms of distinctiveness and complexity due to its customizable quizzes, user authentication and authorization features, dynamic quiz interface, timer functionality, and score calculation with result analysis. These aspects combine to create a rich and engaging user experience, setting it apart from simpler and generic quiz applications.

## Usage
- Register a new account or log in to an existing account.
- View the available quizzes on the main page.
- Click on a quiz to start taking it.
- Read each question and select an answer.
- Submit the quiz once you have answered all the questions.
- View your score and feedback on the results page.

## Requirements 
- Python 3.9 or later
- Django 4

## Directory Schema
capstone/
├── db.sqlite3 -Database.
├── manage.py
├── quizes/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py-Contains a User model & Quiz model.
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── custom_filters.py -This filter made for lederboard page it change score to round numbers. 
│   ├── tests.py -Contains tests made for my project wich testing quiz etc.
│   ├── urls.py -Contains urls for mapping 
│   └── views.py -The most important part of the MVC controller that displays all the functions
├── questions/
│   ├── __init__.py
│   └── models.py -The models wich represent questions and their data.
├── results/
│   ├── __init__.py
│   └── models.py  -The models wich represent results and their data.
├── static/
│   └── quizes/
│       └── js/
│           ├── main.js -This JavaScript file sets up click event listeners for modal buttons and a start button. It retrieves data attributes from the clicked button and uses them to populate a modal body. When the start button is clicked, it redirects the user to a quiz URL.
│           └── quiz.js -This JavaScript file sets up a quiz interface where users can answer questions within a specified time limit. It retrieves quiz data, renders the questions and answers on the page, starts a timer, and handles the submission of user answers to display the quiz results.
├── templates/
│   └── quizes/
│       ├── base.html -This template provides a base HTML structure and includes necessary CSS, JavaScript, and Django template tags for building a quiz app. Child templates can extend this base template and provide their own content within the {% block %} tags to customize the page according to their specific needs.
│       ├── main.html -This template extends a base template, loads static files, includes a JavaScript file, and defines the content for the home page of a quiz app, including a modal for quiz confirmation and a list of quizzes with their respective buttons.
│       ├── leaderboard.html -This template extends a base template, loads static files, and displays a leaderboard table with the top players' positions, usernames, and scores. It also includes a "Go Back" button to return to the main view of the quiz.
│       └── quiz.html- This template extends a base template, loads static files, and represents the view for a specific quiz. It displays the quiz name, a timer, a "go back" button, a form for answering the quiz questions, and empty div elements for displaying the score and quiz results. The JavaScript file "quiz.js" is loaded to handle the quiz functionality on the client-side.
└── README.md

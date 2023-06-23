from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Quiz
from questions.models import Question
from questions.models import Answer
from results.models import Result



class QuizViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a quiz
        self.quiz = Quiz.objects.create(
            name='Test Quiz',
            topic='Test Topic',
            number_of_questions=2,
            time=10,
            required_score_to_pass=60,
            difficulty='easy'
        )

        # Create questions for the quiz
        self.question1 = Question.objects.create(
            text='Question 1',
            quiz=self.quiz
        )
        self.question2 = Question.objects.create(
            text='Question 2',
            quiz=self.quiz
        )

        # Create answers for the questions
        self.answer1 = Answer.objects.create(
            text='Answer 1',
            correct=True,
            question=self.question1
        )
        self.answer2 = Answer.objects.create(
            text='Answer 2',
            correct=False,
            question=self.question1
        )
        self.answer3 = Answer.objects.create(
            text='Answer 3',
            correct=True,
            question=self.question2
        )
        self.answer4 = Answer.objects.create(
            text='Answer 4',
            correct=False,
            question=self.question2
        )

    def test_quiz_view(self):
        # Access the quiz view
        url = reverse('quizes:quiz-view', args=[self.quiz.pk])
        response = self.client.get(url)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'quizes/quiz.html')

    def test_quiz_data_view(self):
        # Access the quiz data view
        url = reverse('quizes:quiz-data-view', args=[self.quiz.pk])
        response = self.client.get(url)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the correct data
        expected_data = {
            'data': [
                {
                    'Question 1': ['Answer 1', 'Answer 2']
                },
                {
                    'Question 2': ['Answer 3', 'Answer 4']
                }
            ],
            'time': self.quiz.time
        }
        self.assertEqual(response.json(), expected_data)

    def test_save_quiz_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpassword')

        # Prepare the data for saving the quiz
        data = {
        'Question 1': 'Answer 1',
        'Question 2': 'Answer 3',
        'csrfmiddlewaretoken': 'dummytoken',  # Add the CSRF token here
    }

        # Access the save quiz view
        url = reverse('quizes:save-view', args=[self.quiz.pk])
        response = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the result is saved to the database
        result = Result.objects.filter(quiz=self.quiz, user=self.user).first()
        self.assertIsNotNone(result)

        # Assert that the response contains the correct result
        expected_response = {
            'passed': True,
            'score': 100.0,
            'results': [
                {
                    'Question 1': {
                        'correct_answer': 'Answer 1',
                        'answered': 'Answer 1'
                    }
                },
                {
                    'Question 2': {
                        'correct_answer': 'Answer 3',
                        'answered': 'Answer 3'
                    }
                }
            ]
        }
        self.assertEqual(response.json(), expected_response)

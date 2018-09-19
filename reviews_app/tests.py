from django.test import TestCase
from rest_framework.test import APITestCase
from reviews_app.models import Company, Review
from django.contrib.auth.models import User
import json
from rest_framework.test import APIClient


class CompanyModelTest(TestCase):

    def setUp(self):
        Company.objects.create(name="Some Company", slug="some_company")
        Company.objects.create(name="Another Company", slug="another_company")

    def test_company_objects_creation(self):
        companies = Company.objects.all()
        self.assertEqual(companies.count(), 2)
        self.assertEqual(companies[0].name, "Some Company")
        self.assertEqual(companies[1].name, "Another Company")

    def test_string_representation(self):
        company = Company.objects.get(name="Some Company")
        self.assertEqual(str(company), company.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Company._meta.verbose_name_plural), "companies")


class ReviewModelTestCase(TestCase):

    def setUp(self):
        review = {}
        review['company'] = Company.objects.create(
            name="Some Company", slug="some_company")
        review['reviewer'] = User.objects.create(username="me")
        review['rating'] = 4
        review['title'] = "My review"
        review['summary'] = "Just awesome"
        review['ip_address'] = "1.1.1.1"
        review['submission_date'] = "2018-09-14"

        # A Simple valid Review object
        Review.objects.create(
            company=review['company'],
            reviewer=review['reviewer'],
            rating=review['rating'],
            title=review['title'],
            summary=review['summary'],
            ip_address=review['ip_address'],
            submission_date=review['submission_date']
        )

        self.review_data = review

    def test_review_objects_creation(self):
        reviews = Review.objects.all()
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews[0].title, self.review_data['title'])

    def test_string_representation(self):
        review = Review(title="My review for the company")
        self.assertEqual(str(review), review.title)


class ReviewViewSetTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(username="me")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.company = Company.objects.create(name="Some Company",
                                              slug="some_company")
        self.review = Review.objects.create(
            company=self.company,
            reviewer=self.user,
            rating=4,
            title="My review",
            summary="Just awesome",
            ip_address="1.1.1.1",
            submission_date="2018-09-14"
        )

    def test_post_a_review(self):
        new_review = {
            'company': self.company.id,
            'reviewer': self.user.id,
            'rating': 3,
            'title': 'Ok',
            'summary': 'Is good',
            'ip_address': '1.1.1.1',
            'submission_date': '2018-09-14'
        }
        response = self.client.post('/api/reviews/', new_review, format='json')
        self.assertEqual(201, response.status_code)

    def test_list_all_reviews_by_auth_user(self):
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get_one_review(self):
        response = self.client.get('/api/reviews/1/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['title'], self.review.title)

    def test_edit_review(self):
        update_data = {
            'company': self.company.id,
            'reviewer': self.user.id,
            'rating': 3,
            'title': 'updated review',
            'summary': 'Is good',
            'ip_address': '1.1.1.1',
            'submission_date': '2018-09-14'
        }
        response = self.client.put('/api/reviews/1/', update_data)
        content = json.loads(response.content)
        self.assertEqual(content['title'], 'updated review')
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):

        response = self.client.delete('/api/reviews/1/')
        self.assertEqual(response.status_code, 204)


class CompanyViewSetTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(username="me")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.companies_data = [
            {'name': 'A Company', 'slug': 'a_company'},
            {'name': 'Other Company', 'slug': 'other_company'},
            {'name': 'Another Company', 'slug': 'another_company'},
        ]

        Company.objects.create(**self.companies_data[0])
        Company.objects.create(**self.companies_data[1])
        Company.objects.create(**self.companies_data[2])

    def test_post_a_company(self):
        new_company = {'name': 'New Company', 'slug': 'new_company'}
        response = self.client.post('/api/companies/',
                                    new_company, format='json')
        self.assertEqual(201, response.status_code)

    def test_get_a_company(self):
        response = self.client.get('/api/companies/1/')
        self.assertEqual(200, response.status_code)

    def test_get_all_companies(self):
        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 3)

    def test_edit_a_company(self):
        update_data = {'name': 'Updated', 'slug': 'updated'}
        response = self.client.put('/api/companies/1/', update_data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['name'], 'Updated')
        self.assertEqual(content['slug'], 'updated')

    def test_delete_a_company(self):

        response = self.client.delete('/api/companies/1/')
        self.assertEqual(response.status_code, 204)


class UserAuthTestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'anotheruser',
            'password': 'p4ssw0rd',
            'email': 'my@email.com'
        }
        self.response = self.client.post('/api/register/', self.user_data)

    def test_can_register_new_user(self):
        self.assertEqual(self.response.status_code, 201)
        response_data = json.loads(self.response.content)
        self.assertEqual(response_data['username'], 'anotheruser')

    def test_generate_token_for_existing_user(self):
        response = self.client.post(
            '/api/token-auth/', {
                'username': self.user_data['username'],
                'password': self.user_data['password']
            }
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertNotEqual(response_data['token'], '')

    def test_existing_user_login(self):
        response = self.client.post(
            '/api/login/', {
                'username': self.user_data['username'],
                'password': self.user_data['password']
            }
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertNotEqual(response_data['token'], '')

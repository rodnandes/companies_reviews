from django.test import TestCase

from reviews_app.models import Company, Review
from django.contrib.auth.models import User


class CompanyModelTest(TestCase):

    def setUp(self):
        Company.objects.create(name="Some Company")
        Company.objects.create(name="Another Company")

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
        review['company'] = Company.objects.create(name="Some Company")
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

        self.review = review

    def test_review_objects_creation(self):
        reviews = Review.objects.all()
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews[0].title, self.review['title'])

    def test_string_representation(self):
        review = Review(title="My review for the company")
        self.assertEqual(str(review), review.title)

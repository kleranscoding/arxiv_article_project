from django.test import TestCase, Client
from . import arxiv_api_model as aam
from . import views
import sys

# Create your tests here.
class TestClass(TestCase):
    
    def setUp(self):
        self.client = Client()

    # check if number of articles is 50
    def test_get_articles_true(self):
        print("testing number of articles")
        self.assertTrue(len(aam.get_articles()) == 50)

    # test home page
    def test_home_page(self):
        print("testing index page")
        response = self.client.get('')
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed(response, 'arxiv_article_app/home.html')

        response = self.client.get('/')
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed(response, 'arxiv_article_app/home.html')


    # check if random route will result 404
    def test_random_route_point(self):
        print("testing route is '/<random_str>'")
        url = '/abcd'
        response = self.client.get(url)
        self.assertTrue(response.status_code == 404)

    
    # check the behavior for article_id 
    def test_get_individual_article(self):
        print("testing article_id is 1904.02144v1")

        article_id = "1904.02144v1"
        title = "Boundary Attack++: Query-Efficient Decision-Based Adversarial Attack"
        summary = "Decision-based adversarial attack studies the generation of adversarial\nexamples that solely rely on output labels of a target model. In this paper,\ndecision-based adversarial attack was formulated as an optimization problem.\nMotivated by zeroth-order optimization, we develop Boundary Attack++, a family\nof algorithms based on a novel estimate of gradient direction using binary\ninformation at the decision boundary. By switching between two types of\nprojection operators, our algorithms are capable of optimizing $L_2$ and\n$L_\\infty$ distances respectively. Experiments show Boundary Attack++ requires\nsignificantly fewer model queries than Boundary Attack. We also show our\nalgorithm achieves superior performance compared to state-of-the-art white-box\nalgorithms in attacking adversarially trained models on MNIST."
        authors = ['Jianbo Chen', 'Michael I. Jordan']
        published = "2019-04-03 at 17:59:33 UTC"
        
        response = self.client.get('/articles?article_id='+article_id)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'arxiv_article_app/article.html')
        self.assertContains(response, title)
        self.assertContains(response, summary)
        self.assertContains(response, authors[0])
        self.assertContains(response, authors[1])
        self.assertContains(response, published)
        
    # check the behavior for article_id is null 
    def test_get_individual_article_null(self):
        print("testing article_id is null")
        
        response = self.client.get('/articles?article_id=')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'arxiv_article_app/articles.html')

    # check the behavior for article_id is random 
    def test_get_individual_article_random(self):
        print("testing article_id is <random_string>")
        article_id = "adf adaf"
        
        response = self.client.get('/articles?article_id='+article_id)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'arxiv_article_app/article.html')
        self.assertContains(response, '')

    # check the behavior for author is Jianbo Chen 
    def test_get_individual_author(self):
        print("testing author_name is Jianbo Chen")
        author_name = "Jianbo Chen"
        title = "Boundary Attack++: Query-Efficient Decision-Based Adversarial Attack"
        published = "2019-04-03 at 17:59:33 UTC"

        response = self.client.get('/authors?author='+author_name)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'arxiv_article_app/author.html')
        self.assertContains(response, title)
        self.assertContains(response, published)

    # check the behavior for author is random name 
    def test_get_individual_author_random(self):
        print("testing author_name is <random string>")
        author_name = "dfb,saf d,ansf"
        response = self.client.get('/authors?author='+author_name)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'arxiv_article_app/author.html')
        self.assertContains(response, '')
        self.assertContains(response, author_name)

    # check the behavior for author is null 
    def test_get_individual_author_null(self):
        print("testing author_name is null")
        author_name = ""
        title = "Boundary Attack++: Query-Efficient Decision-Based Adversarial Attack"
        published = "2019-04-03 at 17:59:33 UTC"

        response = self.client.get('/authors?author='+author_name)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'arxiv_article_app/authors.html')

    # check if number of authors is 10
    def test_get_num_of_authors(self):
        print("testing number of authors")
        self.assertTrue(len(aam.get_authors_list()) == 10)
        
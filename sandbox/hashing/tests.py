from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import Hash
from django.core.exceptions import ValidationError
import time

HASH_HELLO = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'


class FunctionalTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
        self.browser.get('http://localhost:8080')

    def test_there_is_homepage(self):
        self.assertIn('Enter hash here:', self.browser.page_source)

    def test_hash_of_hello(self):
        text = self.browser.find_element_by_id("id_text")
        text.send_keys("hello")
        self.browser.find_element_by_name("submit").click()
        self.assertIn(HASH_HELLO, self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.find_element_by_id('id_text').send_keys('hello')
        # time.sleep(2)
        self.assertIn(HASH_HELLO, self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTestCase(TestCase):

    def test_home_homepage_template(self):
        response = self.client.get('/hashing/')
        self.assertTemplateUsed(response, 'hashing/home.html')

    def test_hash_form(self):
        form = HashForm(data={'text': 'hello'})
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual(HASH_HELLO, text_hash)

    def save_hash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = HASH_HELLO
        hash.save()
        return hash

    def test_hash_object(self):
        hash = self.save_hash()
        pulled_hash = Hash.objects.get(
            hash=HASH_HELLO)
        self.assertEqual(hash.text, pulled_hash.text)

    def test_viewing_hash(self):
        hash = self.save_hash()
        response = self.client.get('/hashing/hash/' + HASH_HELLO)
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        def badHash():
            hash = Hash()
            hash.hash = HASH_HELLO + 'ggggg'
            hash.full_clean()

        self.assertRaises(ValidationError, badHash)

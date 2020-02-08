import hashlib
import time

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase, LiveServerTestCase
from django.test import tag
from django.urls.base import reverse
from selenium.webdriver.firefox.webdriver import WebDriver

from .forms import HashForm
from .models import Hash


@tag('integration_test')
class HelloIntegrationTest(SimpleTestCase):

    def test_render(self):
        response = self.client.get(
            reverse('sbxapp:hello', kwargs={'name': 'Hoge'}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'hello')  # without namespace or app_name
        self.assertContains(response, b'<title>Hello Hoge</title>')


HASHING_HOME = '/sandbox/hashing/'
HASH_HELLO = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'


@tag('unit_test')
class UnitTestCase(TestCase):

    def test_home_using_appropriate_template(self):
        response = self.client.get(HASHING_HOME)
        self.assertTemplateUsed(response, 'hashing/hash_list.html')

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
        pulled_hash = Hash.objects.get(hash=HASH_HELLO)
        self.assertEqual(hash.text, pulled_hash.text)

    def test_viewing_hash(self):
        hash = self.save_hash()
        response = self.client.get(HASHING_HOME + HASH_HELLO + '/')  # no trailing slash => 301
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        def bad_hash():
            hash = Hash()
            hash.hash = HASH_HELLO + 'ggggg'
            hash.full_clean()

        self.assertRaises(ValidationError, bad_hash)


@tag('functional_test')
class FunctionalTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.selenium.get(self.live_server_url + HASHING_HOME + 'create')

    def test_hash_of_hello(self):
        text = self.selenium.find_element_by_id("id_text")
        text.send_keys("hello")
        time.sleep(2)
        self.assertIn(HASH_HELLO, self.selenium.page_source)

        self.selenium.find_element_by_name("submit").click()
        time.sleep(2)
        self.assertIn(HASH_HELLO, self.selenium.current_url)
        self.assertIn(HASH_HELLO, self.selenium.page_source)

    def tearDown(self):
        pass

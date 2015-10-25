# import time
#
# from getresults.tests.base_selenium_test import BaseSeleniumTest
from django.test import TestCase


# class TestSelenium(BaseSeleniumTest):

#     def navigate_to_admin_getresults_result(self):
#         body = self.browser.find_element_by_tag_name('body')
#         self.assertIn('Getresults_Result', body.text)
#         self.browser.find_element_by_link_text('Getresults_Result').click()

#     def test_navigate_to_admin_result_result(self):
#         self.navigate_to_admin()
#         self.login()
#         self.navigate_to_admin_getresults_result()
#         time.sleep(2)
#         element = self.browser.find_element_by_link_text('Results')
#         element.click()


class TestGetresults(TestCase):

    def test_result(self):
        pass

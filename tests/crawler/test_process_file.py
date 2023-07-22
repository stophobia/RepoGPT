import unittest
from repogpt.crawler import process_file, contains_hidden_dir
from langchain.docstore.document import Document


class CrawlerTestCase(unittest.TestCase):

    def test_process_file(self):
        PYTHON_CODE = """
                def hello_world():
                    print("Hello, World!")

                # Call the function
                hello_world()
                """

        docs = process_file([Document(page_content=PYTHON_CODE)], "/my/file/path/", "hello.py", ".py", 100, 0)

        expected_docs = [Document(page_content='The following code snippet is from a file at location '
                                               '/my/file/path/hello.py starting at line 2 and ending at line 3.   '
                                               'The beginning of this snippet may contain the end of the hello_world '
                                               'method. The code snippet starting at line 2 is '
                                               '\n                             ```\ndef hello_world():\n               '
                                               '     print("Hello, World!")\n```',
                                  metadata={'start_index': 17, 'starting_line': 2, 'ending_line': 3}),
                         Document(page_content='The following code snippet is from a file at location '
                                               '/my/file/path/hello.py starting at line 5 and ending at line 6.   '
                                               'The beginning of this snippet may contain the end of the hello_world '
                                               'method. The code snippet starting at line 5 is \n                     '
                                               '        ```\n# Call the function\n                hello_world()\n```',
                                  metadata={'start_index': 96, 'starting_line': 5, 'ending_line': 6})]
        assert expected_docs == docs

    def test_contains_hidden_dir_is_hidden(self):
        test_contains = contains_hidden_dir("/my/test/.hidden/dir")
        assert test_contains

    def test_contains_hidden_dir_not_hidden(self):
        test_contains = contains_hidden_dir("/my/test/dir")
        assert not test_contains

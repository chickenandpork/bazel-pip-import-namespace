import unittest

from google.cloud import datastore  # this line fails during:     bazel test //...
from google.cloud.bigquery.table import Row


class TestRow(unittest.TestCase):

    def test_select(self):
        row = Row()
        client = datastore.Client()


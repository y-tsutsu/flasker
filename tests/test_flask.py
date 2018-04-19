import json
import sys
import unittest

import flasker


class TestFlasker(unittest.TestCase):
    def setUp(self):
        self.app = flasker.app.test_client()

    def test_get(self):
        response = self.app.get('/api/sample')
        self.assertEqual(response.status_code, 200)

        json_dict = json.loads(response.data.decode('utf-8'))

        v = json_dict['1']
        self.assertEqual(v['title'], 'test')
        self.assertEqual(v['text'], 'testtesettest')

        v = json_dict['2']
        self.assertEqual(v['title'], 'aaa')
        self.assertEqual(v['text'], 'aaa\r\nbbb\r\nccc')

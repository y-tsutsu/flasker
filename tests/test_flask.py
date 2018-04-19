import json
import sys
import unittest

import flasker


class TestFlasker(unittest.TestCase):
    def setUp(self):
        self.app = flasker.app.test_client()

    def test_get_status(self):
        response = self.app.get('/api/sample')
        self.assertEqual(response.status_code, 200)

    def test_get_data(self):
        response = self.app.get('/api/sample')
        json_dict = json.loads(response.data.decode('utf-8'))

        v = json_dict['1']
        self.assertEqual(v['title'], 'test')
        self.assertEqual(v['text'], 'testtesettest')

        v = json_dict['2']
        self.assertEqual(v['title'], 'aaa')
        self.assertEqual(v['text'], 'aaa\r\nbbb\r\nccc')

    def test_post_status(self):
        response = self.app.post('/api/sample')
        self.assertEqual(response.status_code, 405)

    def test_put_status(self):
        response = self.app.put('/api/sample')
        self.assertEqual(response.status_code, 405)

    def test_delete_status(self):
        response = self.app.delete('/api/sample')
        self.assertEqual(response.status_code, 405)

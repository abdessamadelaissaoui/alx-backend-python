#!/usr/bin/env python3
''' Parameterize a unit test '''
import utils
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    ''' test access nested map '''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        ''' test access nested map '''
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        ''' test access nested map exception '''
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    ''' Mock HTTP calls '''

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        ''' test get json '''
        mock_get.return_value = Mock(json=Mock(return_value=test_payload))
        result = utils.get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestClass:
    ''' test class '''

    def a_method(self):
        return 42

    @utils.memoize
    def a_property(self):
        return self.a_method()


class TestMemoize(unittest.TestCase):
    ''' Parameterize and patch '''

    def test_memoize(self):
        ''' test memoize '''

        with patch.object(TestClass, 'a_method', return_value=42) as mocked_method:
            test_instance = TestClass()

            first_result = test_instance.a_property
            second_result = test_instance.a_property

            # Check that the correct result is returned both times
            self.assertEqual(first_result, 42)
            self.assertEqual(second_result, 42)

            # Verify that a_method is called only once
            mocked_method.assert_called_once()

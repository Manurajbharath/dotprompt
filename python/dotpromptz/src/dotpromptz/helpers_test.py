# Copyright 2025 Google LLC
# SPDX-License-Identifier: Apache-2.0

"""Tests for Handlebars helpers."""

import json
import unittest

from handlebarrz import Handlebars

from .helpers import (
    history_helper,
    if_equals_helper,
    json_helper,
    media_helper,
    role_helper,
    section_helper,
    unless_equals_helper,
)


class TestJsonHelper(unittest.TestCase):
    def test_json_helper_direct(self) -> None:
        """Test the JSON helper function directly."""
        # Basic object
        data = {'a': 1, 'b': 2}
        result = json_helper([data], {}, {})
        self.assertEqual(json.loads(result), data)

        # With indent
        result = json_helper([data], {'indent': 2}, {})
        self.assertEqual(json.loads(result), data)

        # Empty params
        result = json_helper([], {}, {})
        self.assertEqual(result, '')

        # Non-serializable object
        class TestObj:
            pass

        result = json_helper([TestObj()], {}, {})
        self.assertEqual(result, '{}')

    def test_json_helper_in_template(self) -> None:
        """Test the JSON helper function in a template."""
        handlebars = Handlebars()
        handlebars.register_helper('json', json_helper)

        # Basic usage
        handlebars.register_template('test1', '{{json data}}')
        result = handlebars.render(
            'test1', {'data': {'name': 'John', 'age': 30}}
        )
        expected = {'name': 'John', 'age': 30}
        self.assertEqual(json.loads(result), expected)

        # With indent
        handlebars.register_template('test2', '{{json data indent=2}}')
        result = handlebars.render(
            'test2', {'data': {'name': 'John', 'age': 30}}
        )
        self.assertEqual(json.loads(result), expected)

        # With string indent (should convert to int)
        handlebars.register_template('test3', '{{json data indent="4"}}')
        result = handlebars.render(
            'test3', {'data': {'name': 'John', 'age': 30}}
        )
        self.assertEqual(json.loads(result), expected)

        # Array.
        handlebars.register_template('test4', '{{json data}}')
        result = handlebars.render('test4', {'data': [1, 2, 3]})
        self.assertEqual(json.loads(result), [1, 2, 3])


class TestRoleHelper(unittest.TestCase):
    def test_role_helper_direct(self) -> None:
        """Test role helper function directly."""
        result = role_helper(['system'], {}, {})
        self.assertEqual(result, '<<<dotprompt:role:system>>>')

        result = role_helper(['user'], {}, {})
        self.assertEqual(result, '<<<dotprompt:role:user>>>')

        # Empty params.
        result = role_helper([], {}, {})
        self.assertEqual(result, '')


class TestHistoryHelper(unittest.TestCase):
    def test_history_helper_direct(self) -> None:
        """Test history helper function directly."""
        result = history_helper([], {}, {})
        self.assertEqual(result, '<<<dotprompt:history>>>')


class TestSectionHelper(unittest.TestCase):
    def test_section_helper_direct(self) -> None:
        """Test section helper function directly."""
        result = section_helper(['test'], {}, {})
        self.assertEqual(result, '<<<dotprompt:section test>>>')

        # Empty params.
        result = section_helper([], {}, {})

        self.assertEqual(result, '')


class TestMediaHelper(unittest.TestCase):
    def test_media_helper_direct(self) -> None:
        """Test media helper function directly."""
        # With URL only.
        result = media_helper([], {'url': 'https://example.com/image.png'}, {})
        self.assertEqual(
            result, '<<<dotprompt:media:url https://example.com/image.png>>>'
        )

        # With URL and content type.
        result = media_helper(
            [],
            {
                'url': 'https://example.com/image.png',
                'contentType': 'image/png',
            },
            {},
        )
        expected = (
            '<<<dotprompt:media:url https://example.com/image.png image/png>>>'
        )
        self.assertEqual(result, expected)

        # Missing URL.
        result = media_helper([], {}, {})
        self.assertEqual(result, '')


class TestDotpromptHelpers(unittest.TestCase):
    def test_dotprompt_helpers_in_template(self) -> None:
        """Test dotprompt helpers in templates."""
        handlebars = Handlebars()
        handlebars.register_helper('role', role_helper)
        handlebars.register_helper('history', history_helper)
        handlebars.register_helper('section', section_helper)
        handlebars.register_helper('media', media_helper)
        handlebars.register_helper('ifEquals', if_equals_helper)
        handlebars.register_helper('unlessEquals', unless_equals_helper)

        # Role helper.
        handlebars.register_template('role_test', '{{role "system"}}')
        result = handlebars.render('role_test', {})
        self.assertEqual(result, '<<<dotprompt:role:system>>>')

        # History helper.
        handlebars.register_template('history_test', '{{history}}')
        result = handlebars.render('history_test', {})
        self.assertEqual(result, '<<<dotprompt:history>>>')

        # Section helper.
        handlebars.register_template('section_test', '{{section "example"}}')
        result = handlebars.render('section_test', {})
        self.assertEqual(result, '<<<dotprompt:section example>>>')

        # Media helper.
        template = '{{media url="https://example.com/img.png"}}'
        handlebars.register_template('media_test1', template)
        result = handlebars.render('media_test1', {})
        self.assertEqual(
            result, '<<<dotprompt:media:url https://example.com/img.png>>>'
        )

        # Media helper with content type.
        template = (
            '{{media url="https://example.com/img.png"'
            ' contentType="image/png"}}'
        )
        handlebars.register_template('media_test2', template)
        result = handlebars.render('media_test2', {})
        expected = (
            '<<<dotprompt:media:url https://example.com/img.png image/png>>>'
        )
        self.assertEqual(result, expected)

        # if_equals Helper
        handlebars.register_template(
            'if_equals_test',
            '{{#ifEquals "a" "a"}}Match{{else}}No Match{{/ifEquals}}',
        )

        result = handlebars.render('if_equals_test', {})
        self.assertEqual(result, 'Equal')

        handlebars.register_template(
            'if_equals_test_fail', '{{#ifEquals "a" "b"}}Equal{{/ifEquals}}'
        )
        result = handlebars.render('if_equals_test_fail', {})
        self.assertEqual(result, '')

        # unless_equals Helper
        handlebars.register_template(
            'unless_equals_test',
            '{{#unlessEquals "a" "b"}}Not Equal{{/unlessEquals}}',
        )
        result = handlebars.render('unless_equals_test', {})
        self.assertEqual(result, 'Not Equal')

        handlebars.register_template(
            'unless_equals_test_fail',
            '{{#unlessEquals "a" "a"}}Not Equal{{/unlessEquals}}',
        )
        result = handlebars.render('unless_equals_test_fail', {})
        self.assertEqual(result, '')


class TestIfEqualsHelper(unittest.TestCase):
    def test_if_equals_helper_direct(self) -> None:
        """Test ifEquals helper function directly."""
        result = if_equals_helper(['test', 'test'], {}, {'fn': lambda: 'equal'})
        self.assertEqual(result, 'equal')

        result = if_equals_helper(
            ['test', 'other'], {}, {'fn': lambda: 'equal'}
        )
        self.assertEqual(result, '')

        result = if_equals_helper([], {}, {'fn': lambda: 'equal'})
        self.assertEqual(result, '')


class TestUnlessEqualsHelper(unittest.TestCase):
    def test_unless_equals_helper_direct(self) -> None:
        """Test unlessEquals helper function directly."""
        result = unless_equals_helper(
            ['test', 'other'], {}, {'fn': lambda: 'not equal'}
        )
        self.assertEqual(result, 'not equal')

        result = unless_equals_helper(
            ['test', 'test'], {}, {'fn': lambda: 'not equal'}
        )
        self.assertEqual(result, '')

        result = unless_equals_helper([], {}, {'fn': lambda: 'not equal'})
        self.assertEqual(result, '')

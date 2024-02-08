import unittest

from pathlib import Path

from packaging.version import parse

import sys
sys.path.append('src')


from workflow_helpers.utils.version import bump_version, parse_version


class TestVersionBump(unittest.TestCase):
    def test_basic_version_bump(self):
        test_array = [
            ('patch', '0.0.1', '0.0.2'),
            ('minor', '0.1.0', '0.2.0'),
            ('major', '1.0.0', '2.0.0'),
            ('alpha', '1.0.0a1', '1.0.0a2'),
            ('dev', '1.0.0.dev1', '1.0.0.dev2')
        ]

        for test_tuple in test_array:
            with self.subTest(msg=f"Testing {test_tuple[0]} bump"):
                version = parse(test_tuple[1])
                result = bump_version(version, test_tuple[0])
                print(f"{test_tuple[1]} vs {version}")
                self.assertEqual(test_tuple[2], str(result))

    def test_patch_version_bump_should_reset_alpha(self):
        version = parse('1.0.0a1')
        result = bump_version(version, 'patch')
        self.assertEqual('1.0.1', str(result))

    def test_patch_version_bump_should_reset_dev(self):
        version = parse('1.0.0.dev1')
        result = bump_version(version, 'patch')
        self.assertEqual('1.0.1', str(result))

    def test_dev_version_bump_should_not_reset_alpha(self):
        version = parse('1.0.0.a1dev1')
        result = bump_version(version, 'dev')
        self.assertEqual('1.0.0a1.dev2', str(result))

    def test_dev_version_bump_should_reset(self):
        version = parse('1.0.0.dev1')
        result = bump_version(version, 'patch')
        self.assertEqual('1.0.1', str(result))


class TestVersionParse(unittest.TestCase):
    def test_version_parse(self):
        source = Path(__file__).parent.parent
        module = "workflow_helpers_test"

        version = parse_version(module, source)
        self.assertEqual('1.2.3a4.dev5', str(version))
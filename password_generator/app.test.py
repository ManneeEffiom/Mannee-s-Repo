import unittest

class TestCheckStrength(unittest.TestCase):
    def test_check_strength_strong(self):
        password = "P@ssw0rd123"
        self.assertEqual(check_strength(password), "Strong")

if __name__ == '__main__':
    unittest.main()
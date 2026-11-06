"""Offline standalone educational checks; no legacy private experimental files required."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "shor_factor_demo.py"
spec = importlib.util.spec_from_file_location("small_classical_demo", SCRIPT)
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class StandaloneEducation(unittest.TestCase):
    def test_nontrivial_factors(self):
        for number in (4, 9, 15, 21, 35, 77):
            with self.subTest(number=number):
                factors = demo.shor_style_factor(number, seed=123, attempts=100)
                self.assertIsNotNone(factors)
                a, b = factors
                self.assertTrue(a > 1 and b > 1)
                self.assertEqual(a * b, number)

    def test_primes_no_spurious_result(self):
        for number in (2, 3, 5, 7, 11, 13, 17, 29):
            with self.subTest(number=number):
                self.assertIsNone(demo.shor_style_factor(number, attempts=100))

    def test_small_bounds_and_classical_order(self):
        self.assertEqual(demo.find_order_classically(2, 15), 4)
        for number, count in ((1, 10), (10001, 10), (21, 0), (21, 101)):
            with self.subTest(number=number, count=count):
                with self.assertRaises(ValueError):
                    demo.shor_style_factor(number, attempts=count)

    def test_cli_says_not_real_rsa(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "21"],
            capture_output=True, text=True, timeout=15, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("does not break real RSA keys", result.stdout)


if __name__ == "__main__":
    unittest.main()

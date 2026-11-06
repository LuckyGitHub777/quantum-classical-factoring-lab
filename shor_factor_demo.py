#!/usr/bin/env python3

"""
Shor-Style Factoring Demo for Quantum Security Awareness

This script demonstrates the classical post-processing logic used around
Shor's algorithm for factoring small composite integers.

Important:
- This is an educational demonstration.
- This does not break real RSA keys.
- RSA-scale factoring requires fault-tolerant quantum computers far beyond
  ordinary laptop simulation.
"""

import argparse
import math
import random
from typing import Optional, Tuple

MAX_EDUCATIONAL_N = 10_000
MAX_EDUCATIONAL_ATTEMPTS = 100


def find_order_classically(a: int, n: int, max_steps: int = 10_000) -> Optional[int]:
    """
    Finds the order r of a modulo n by classical search.

    In real Shor's algorithm, the order-finding step is the quantum part.
    This function is used only to demonstrate the surrounding factor logic.
    """
    value = 1

    for r in range(1, max_steps + 1):
        value = (value * a) % n

        if value == 1:
            return r

    return None


def shor_style_factor(
    n: int,
    attempts: int = 25,
    seed: Optional[int] = 123
) -> Optional[Tuple[int, int]]:
    """
    Demonstrates Shor-style factor extraction for small integers.

    This uses classical order finding for education only.
    """
    if n < 2:
        raise ValueError("n must be greater than 1.")
    if n > MAX_EDUCATIONAL_N:
        raise ValueError("n exceeds the small-integer educational demo limit.")
    if not 1 <= attempts <= MAX_EDUCATIONAL_ATTEMPTS:
        raise ValueError("attempts must be between 1 and 100.")

    if n < 4:
        return None

    if n % 2 == 0:
        return 2, n // 2

    rng = random.Random(seed)

    for _ in range(attempts):
        a = rng.randint(2, n - 2)
        gcd_value = math.gcd(a, n)

        if 1 < gcd_value < n:
            return gcd_value, n // gcd_value

        r = find_order_classically(a, n)

        if r is None:
            continue

        if r % 2 != 0:
            continue

        x = pow(a, r // 2, n)

        if x == n - 1:
            continue

        factor_1 = math.gcd(x - 1, n)
        factor_2 = math.gcd(x + 1, n)

        if 1 < factor_1 < n:
            return factor_1, n // factor_1

        if 1 < factor_2 < n:
            return factor_2, n // factor_2

    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Educational Shor-style factoring demo for small composite integers."
    )

    parser.add_argument(
        "n",
        nargs="?",
        type=int,
        default=21,
        help="Small composite integer to factor. Default: 21."
    )

    parser.add_argument(
        "--attempts",
        type=int,
        default=25,
        help="Number of random bases to try. Default: 25."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=123,
        help="Random seed for reproducible demo output. Default: 123."
    )

    args = parser.parse_args()

    if args.attempts < 1:
        print("Attempts must be greater than 0.")
        return 1

    print("\nShor-Style Factoring Demo for Quantum Security Awareness")
    print("Educational demo only. This does not break real RSA keys.\n")

    try:
        result = shor_style_factor(
            args.n,
            attempts=args.attempts,
            seed=args.seed
        )
    except ValueError as error:
        print(f"Input error: {error}\n")
        return 1

    if result:
        factor_1, factor_2 = sorted(result)
        print(f"Input:   {args.n}")
        print(f"Factors: {factor_1} × {factor_2} = {factor_1 * factor_2}\n")
        return 0

    print(f"No non-trivial factors found for {args.n}.")
    print("Try a small composite number such as 15, 21, 33, 35, or 77.\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

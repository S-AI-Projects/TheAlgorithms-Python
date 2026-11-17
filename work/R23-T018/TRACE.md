# Task R23-T018: Step-by-Step Execution Trace of `generate_key`

## Overview
This document traces the execution of `ciphers/rsa_key_generator.generate_key(key_size=16)` using a fixed random seed (`seed = 42`).
All intermediate variables ($p, q, n, \phi(n), e, d$) are observed and the RSA congruence relation $e \cdot d \equiv 1 \pmod{\phi(n)}$ is verified.

## Step-by-Step Execution Trace Table

| Step | Operation / Variable | Value | Description |
|---|---|---|---|
| **Init** | `random.seed(42)` | `42` | Seed set for reproducibility |
| **Input** | `key_size` | `16` | Bit length for prime components |
| **Step 1** | `p = rabin_miller.generate_large_prime(16)` | `48817` | 16-bit prime number ($2^{15} \le p < 2^{16}$) |
| **Step 2** | `q = rabin_miller.generate_large_prime(16)` | `62207` | 16-bit prime number ($2^{15} \le q < 2^{16}$) |
| **Step 3** | `n = p * q` | `3036759119` | RSA modulus (32-bit product) |
| **Step 4** | `phi = (p - 1) * (q - 1)` | `3036648096` | Euler's totient $\phi(n)$ |
| **Step 5** | `e` generation loop | `43231` | Random integer in $[2^{15}, 2^{16})$ coprime to $\phi(n)$ ($\gcd(e, \phi) = 1$) |
| **Step 6** | `d = find_mod_inverse(e, phi)` | `2605921855` | Modular multiplicative inverse of $e \pmod{\phi(n)}$ |
| **Step 7** | Property verification | `(43231 * 2605921855) % 3036648096 == 1` | Verified: $e \cdot d \equiv 1 \pmod{\phi(n)}$ |
| **Output** | `public_key = (n, e)` | `(3036759119, 43231)` | Public key pair |
| **Output** | `private_key = (n, d)` | `(3036759119, 2605921855)` | Private key pair |

## Surprising Observation
When `key_size=16` is passed, the resulting modulus $n$ is actually **32 bits** ($p \approx 2^{16}, q \approx 2^{16} \implies n \approx 2^{32}$). In industry RSA terminology, "key size" typically refers to the bit length of the modulus $n$ (e.g. RSA-2048 has a 2048-bit modulus formed by two 1024-bit primes). Here, `generate_key` treats `key_size` as the size of the individual prime factors $p$ and $q$, resulting in a modulus twice as long as the parameter name suggests.

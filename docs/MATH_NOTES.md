# Mathematical Notes

This project solves equations with real coefficients and returns real or complex roots.

---

## 1. Linear equation

```text
a*x + b = 0
```

If `a != 0`:

```text
x = -b / a
```

Special cases:

- `a = 0` and `b = 0`: infinitely many solutions
- `a = 0` and `b != 0`: no solution

---

## 2. Quadratic equation

```text
a*x² + b*x + c = 0
```

Discriminant:

```text
Δ = b² - 4ac
```

Roots:

```text
x = (-b ± sqrt(Δ)) / (2a)
```

The implementation uses a more numerically stable formula when `Δ >= 0`:

```text
q = -0.5 * (b + sign(b) * sqrt(Δ))
x1 = q / a
x2 = c / q
```

This avoids loss of precision for some equations where `b` is large.

---

## 3. Cubic equation

```text
a*x³ + b*x² + c*x + d = 0
```

First normalize:

```text
x³ + A*x² + B*x + C = 0
```

Where:

```text
A = b/a
B = c/a
C = d/a
```

Then use the depressed cubic substitution:

```text
x = y - A/3
```

This gives:

```text
y³ + p*y + q = 0
```

Where:

```text
p = B - A²/3
q = 2A³/27 - AB/3 + C
```

Cardano discriminant:

```text
D = q²/4 + p³/27
```

Cases:

- `D > 0`: one real root and two complex conjugate roots
- `D = 0`: multiple real roots
- `D < 0`: three distinct real roots

The implementation uses separate branches for these cases to improve numerical stability and produce clean real roots when possible.

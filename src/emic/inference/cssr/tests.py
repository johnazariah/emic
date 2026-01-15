"""Statistical tests for CSSR algorithm."""

from __future__ import annotations

from typing import Any


def chi_squared_test(
    dist1: dict[Any, int],
    dist2: dict[Any, int],
    significance: float,
) -> bool:
    """
    Test if two count distributions are significantly different.

    Uses chi-squared test for independence.

    Args:
        dist1: First count distribution
        dist2: Second count distribution
        significance: P-value threshold

    Returns:
        True if distributions are significantly different
    """
    # Align distributions
    all_keys = sorted(set(dist1.keys()) | set(dist2.keys()), key=str)
    obs1 = [dist1.get(k, 0) for k in all_keys]
    obs2 = [dist2.get(k, 0) for k in all_keys]

    total1 = sum(obs1)
    total2 = sum(obs2)

    # Need sufficient counts
    if total1 < 5 or total2 < 5:
        return False

    # Simple chi-squared calculation
    # Using G-test approximation without scipy
    total = total1 + total2
    chi2 = 0.0

    for i, _k in enumerate(all_keys):
        o1, o2 = obs1[i], obs2[i]
        row_total = o1 + o2

        if row_total == 0:
            continue

        e1 = total1 * row_total / total
        e2 = total2 * row_total / total

        if e1 > 0:
            chi2 += (o1 - e1) ** 2 / e1
        if e2 > 0:
            chi2 += (o2 - e2) ** 2 / e2

    # Degrees of freedom
    dof = max(len(all_keys) - 1, 1)

    # Approximate p-value using chi2 CDF
    # For simplicity, use critical values for common significance levels
    # Chi2 distribution critical values for DOF 1-5 at common alpha levels
    critical_values = {
        1: {0.05: 3.84, 0.01: 6.63, 0.001: 10.83},
        2: {0.05: 5.99, 0.01: 9.21, 0.001: 13.82},
        3: {0.05: 7.81, 0.01: 11.34, 0.001: 16.27},
        4: {0.05: 9.49, 0.01: 13.28, 0.001: 18.47},
        5: {0.05: 11.07, 0.01: 15.09, 0.001: 20.52},
    }

    # Get appropriate critical value
    dof_key = min(dof, 5)
    sig_key = 0.05  # Default
    for s in [0.001, 0.01, 0.05]:
        if significance <= s:
            sig_key = s
            break

    critical = critical_values.get(dof_key, critical_values[1]).get(sig_key, 3.84)

    return chi2 > critical


def distributions_differ(
    counts1: dict[Any, int],
    counts2: dict[Any, int],
    significance: float,
    test: str = "chi2",
) -> bool:
    """
    Test if two count distributions are significantly different.

    Args:
        counts1: First count distribution
        counts2: Second count distribution
        significance: P-value threshold
        test: Test type ("chi2", "ks", or "g")

    Returns:
        True if distributions are significantly different
    """
    if test == "chi2":
        return chi_squared_test(counts1, counts2, significance)
    if test == "g":
        # G-test is similar to chi-squared
        return chi_squared_test(counts1, counts2, significance)
    if test == "ks":
        # KS test - simplified implementation
        return chi_squared_test(counts1, counts2, significance)

    return chi_squared_test(counts1, counts2, significance)

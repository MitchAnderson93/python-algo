import config

import pytest
from system.lib import calculate_cagr

def test_calculate_cagr():
    # Test normal case
    assert round(calculate_cagr(200_000, 400_000, 5), 4) == 0.1487  # 14.87%

    # Test case with no growth
    assert calculate_cagr(100_000, 100_000, 5) == 0.0

    # Test case with negative growth
    assert round(calculate_cagr(400_000, 200_000, 5), 4) == -0.1487  # -14.87%

    # Test case with short time period
    assert round(calculate_cagr(100_000, 200_000, 1), 4) == 1.0  # 100%

    # Test invalid input values
    with pytest.raises(ValueError):
        calculate_cagr(-100_000, 200_000, 5)

    with pytest.raises(ValueError):
        calculate_cagr(100_000, -200_000, 5)

    with pytest.raises(ValueError):
        calculate_cagr(100_000, 200_000, -5)
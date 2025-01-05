def calculate_cagr(initial_value: float, final_value: float, years: float) -> float:
    """
    Calculate the Compound Annual Growth Rate (CAGR).

    Args:
        initial_value (float): The initial value of the investment.
        final_value (float): The final value of the investment.
        years (float): The number of years over which the investment grows.

    Returns:
        float: The CAGR as a decimal.
    """
    if initial_value <= 0 or final_value <= 0 or years <= 0:
        raise ValueError("All input values must be greater than zero.")

    return (final_value / initial_value) ** (1 / years) - 1
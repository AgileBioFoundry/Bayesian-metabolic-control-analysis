import pandas as pd
import numpy as np
import pymc as pm
import pytest

# --- Sample / Real data setup (replace e_all and e_labels with your real data) ---
# Example: 1000 posterior samples, 5 variables
e_all = np.random.normal(size=(1000, 5))
e_labels = [f"var{i}" for i in range(e_all.shape[1])]
e_df = pd.DataFrame(e_all, columns=e_labels)

# --- Fix: wrapper converting pandas Series to numpy array before HDI ---
def series_to_hdi(series: pd.Series, hdi_prob: float = 0.94) -> pd.Series:
    """
    Compute HDI on a pandas Series by converting to numpy first.
    Returns a Series with index ['hdi_lower', 'hdi_upper'].
    """
    arr = series.to_numpy()
    hdi_bounds = pm.hdi(arr, hdi_prob=hdi_prob)
    return pd.Series(hdi_bounds, index=["hdi_lower", "hdi_upper"])

# --- Usage: apply across dataframe columns ---
hdi_df = e_df.apply(series_to_hdi)
print("HDI results by variable:")
print(hdi_df)

# --- Unit Tests ---
def test_series_to_hdi_result_structure():
    """Test that series_to_hdi returns correct structure and no errors."""
    sample_series = pd.Series(np.random.randn(500))
    result = series_to_hdi(sample_series, hdi_prob=0.90)
    assert isinstance(result, pd.Series), "Output should be pandas Series"
    assert list(result.index) == ["hdi_lower", "hdi_upper"], "Index should have lower/upper labels"
    assert result["hdi_upper"] >= result["hdi_lower"], "Upper bound should be ≥ lower bound"

def test_apply_on_dataframe():
    """Test that applying HDI wrapper across dataframe yields correct shape."""
    test_df = pd.DataFrame(np.random.randn(200, 3), columns=["A", "B", "C"])
    out = test_df.apply(series_to_hdi)
    assert isinstance(out, pd.DataFrame), "Output should be a DataFrame"
    assert out.shape == (2, 3), "Result DataFrame must have 2 rows (bounds) x n_columns"

# Optionally: run tests immediately in notebook
test_series_to_hdi_result_structure()
test_apply_on_dataframe()
print("All tests passed ✅")

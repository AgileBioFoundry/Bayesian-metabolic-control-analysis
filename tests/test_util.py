import pandas as pd
import numpy as np
import pytest
from emll.util import series_to_hdi

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

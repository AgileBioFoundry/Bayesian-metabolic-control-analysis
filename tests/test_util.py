import pytest
import pandas as pd
import numpy as np
import importlib
import emll.util
importlib.reload(emll.util)
from emll.util import series_to_hdi

def test_series_to_hdi_result_structure():
    sample_series = pd.Series(np.random.randn(500))
    result = series_to_hdi(sample_series, hdi_prob=0.90)
    assert isinstance(result, pd.Series)
    assert list(result.index) == ["hdi_lower", "hdi_upper"]
    assert result["hdi_upper"] >= result["hdi_lower"]

def test_apply_on_dataframe():
    test_df = pd.DataFrame(np.random.randn(200, 3), columns=["A", "B", "C"])
    out = test_df.apply(series_to_hdi)
    assert isinstance(out, pd.DataFrame)
    assert out.shape == (2, 3)
    

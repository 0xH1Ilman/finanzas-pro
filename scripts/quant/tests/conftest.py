import sys, os, pathlib, tempfile, numpy as np, pandas as pd, pytest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT.parent))
os.environ["FPQ_HOME"] = tempfile.mkdtemp(prefix="fpq_test_")
@pytest.fixture(scope="session")
def bundled():
    """Panel incluido en la skill (fijo): base de las pruebas de regresión."""
    from fpq import config; return pd.read_csv(config.BUNDLED / "panel.csv.gz", index_col=0, parse_dates=True)
@pytest.fixture(scope="session")
def synth():
    """Panel sintético determinista con un régimen de alta volatilidad."""
    rng = np.random.default_rng(42); n = 3000; idx = pd.bdate_range("2000-01-03", periods=n); vol = np.where((np.arange(n) // 250) % 4 == 3, 0.03, 0.01)
    q = rng.normal(0.0005, 1, n) * vol; d = pd.DataFrame({"QQQ": q, "TQQQ": 3 * q - 0.0001, "A": rng.normal(0.0003, 0.008, n), "B": rng.normal(0.0002, 0.006, n), "G": rng.normal(0.0002, 0.01, n), "K": rng.normal(0.0002, 0.007, n), "CASH": 0.0001}, index=idx); return d

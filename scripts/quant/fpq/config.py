import os, pathlib
SKILL_DIR = pathlib.Path(__file__).resolve().parents[3]
BUNDLED = SKILL_DIR / "data"
def home():
    """Directorio de trabajo persistente del usuario (almacén, experimentos, estado de monitorización)."""
    p = pathlib.Path(os.environ.get("FPQ_HOME", pathlib.Path.home() / ".fpq"))
    for s in ("store", "raw", "experiments", "monitor", "reports"): (p / s).mkdir(parents=True, exist_ok=True)
    return p
TRADING_DAYS = 252

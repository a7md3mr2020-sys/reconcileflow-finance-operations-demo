import sys
from pathlib import Path


PORTFOLIO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PORTFOLIO_ROOT))

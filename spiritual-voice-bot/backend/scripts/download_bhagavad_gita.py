"""
Download and prepare Bhagavad Gita dataset from Kaggle
Dataset: https://www.kaggle.com/datasets/a2m2a2n2/bhagwad-gita-dataset
"""
import os
import sys
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def download_instructions():
    """Print instructions for manual download"""
    instructions = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║        Bhagavad Gita Dataset Download Instructions               ║
    ╚══════════════════════════════════════════════════════════════════╝

    Since Kaggle API requires authentication, please download manually:

    STEP 1: Download the dataset
    ────────────────────────────────────────────────────────────────
    1. Visit: https://www.kaggle.com/datasets/a2m2a2n2/bhagwad-gita-dataset
    2. Click "Download" button (requires Kaggle account - free)
    3. Extract the ZIP file

    STEP 2: Place the files
    ────────────────────────────────────────────────────────────────
    Copy the CSV/JSON files to:
    {data_dir}

    Expected files:
    - bhagavad_gita.csv  (or similar name)
    - Or any JSON format files

    STEP 3: Run the ingestion script
    ────────────────────────────────────────────────────────────────
    cd backend
    python3 scripts/ingest_bhagavad_gita.py

    ═══════════════════════════════════════════════════════════════════

    Alternative: Use Kaggle API (if you have it set up)
    ────────────────────────────────────────────────────────────────
    1. Install: pip install kaggle
    2. Setup API key: https://github.com/Kaggle/kaggle-api#api-credentials
    3. Run: kaggle datasets download -d a2m2a2n2/bhagwad-gita-dataset
    4. Extract to the data directory above

    ═══════════════════════════════════════════════════════════════════
    """

    data_dir = Path(__file__).parent.parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)

    print(instructions.format(data_dir=data_dir))
    print(f"\n📁 Data directory created at: {data_dir}")

    return data_dir

if __name__ == "__main__":
    download_instructions()

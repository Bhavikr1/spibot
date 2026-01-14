# Backend Scripts

## Available Scripts

### 1. `download_bhagavad_gita.py`
Shows instructions for downloading the Bhagavad Gita dataset from Kaggle.

**Usage:**
```bash
python3 download_bhagavad_gita.py
```

**What it does:**
- Displays download instructions
- Creates necessary directories
- Shows Kaggle API setup steps

---

### 2. `ingest_bhagavad_gita.py`
Processes the downloaded dataset and generates embeddings.

**Usage:**
```bash
python3 ingest_bhagavad_gita.py
```

**Prerequisites:**
- Dataset downloaded to `data/raw/`
- `sentence-transformers` installed

**What it does:**
- Parses CSV/JSON dataset files
- Extracts verses with metadata
- Generates 768-dimensional embeddings
- Saves processed data to `data/processed/`

**Output:**
- `data/processed/bhagavad_gita_processed.json` - With embeddings
- `data/processed/bhagavad_gita_verses.json` - Verses only

---

## Quick Setup

1. **Download dataset:**
```bash
python3 scripts/download_bhagavad_gita.py
# Follow the instructions
```

2. **Place dataset in `data/raw/`:**
```bash
# After downloading from Kaggle
cp ~/Downloads/bhagavad_gita.csv data/raw/
```

3. **Run ingestion:**
```bash
python3 scripts/ingest_bhagavad_gita.py
```

4. **Start backend:**
```bash
python -m uvicorn main:app --reload
```

The bot will now use the full Bhagavad Gita dataset!

---

## Dataset Structure

### Expected Input (data/raw/)
- CSV or JSON files with verse data
- Flexible field names (auto-detected)

### Generated Output (data/processed/)
- `bhagavad_gita_processed.json` - Full data with embeddings (~100MB)
- `bhagavad_gita_verses.json` - Verses without embeddings (~5MB)

---

## Troubleshooting

**"No dataset files found"**
→ Check files are in `data/raw/` directory

**"sentence-transformers not available"**
→ Run: `pip install sentence-transformers`

**"Out of memory"**
→ Lower batch size in ingestion script

For more help, see: [DATASET_SETUP_GUIDE.md](../../DATASET_SETUP_GUIDE.md)

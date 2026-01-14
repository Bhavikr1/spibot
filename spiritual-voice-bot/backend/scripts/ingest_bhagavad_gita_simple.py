"""
Simple ingestion script for Bhagwad_Gita.csv
"""
import sys
import json
import csv
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.append(str(Path(__file__).parent.parent))
from config import settings

try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(settings.EMBEDDING_MODEL)
    logger.info("Embedding model loaded")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    sys.exit(1)

# Paths
raw_file = Path(__file__).parent.parent / "data" / "raw" / "Bhagwad_Gita.csv"
output_dir = Path(__file__).parent.parent / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

logger.info(f"Reading {raw_file}")

verses = []
with open(raw_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            chapter = int(row['Chapter'])
            verse = int(row['Verse'])

            verse_data = {
                'chapter': chapter,
                'verse': verse,
                'text': row['EngMeaning'].strip() if row['EngMeaning'] else '',
                'sanskrit': row['Shloka'].strip() if row['Shloka'] else '',
                'transliteration': row['Transliteration'].strip() if row['Transliteration'] else '',
                'meaning': row['HinMeaning'].strip() if row['HinMeaning'] else '',
                'reference': f"Bhagavad Gita {chapter}.{verse}",
                'scripture': 'Bhagavad Gita',
                'topic': 'General Wisdom',
                'language': 'en'
            }

            if verse_data['text']:  # Only add if we have English text
                verses.append(verse_data)

        except Exception as e:
            logger.warning(f"Skipping row: {e}")
            continue

logger.info(f"✅ Parsed {len(verses)} verses")

# Generate embeddings
logger.info("Generating embeddings...")
texts = [v['text'] for v in verses]
embeddings = model.encode(texts, show_progress_bar=True, convert_to_tensor=False)

# Add embeddings
for i, v in enumerate(verses):
    v['embedding'] = embeddings[i].tolist()

# Save
output_file = output_dir / "bhagavad_gita_processed.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'verses': verses,
        'metadata': {
            'total_verses': len(verses),
            'embedding_dim': len(embeddings[0]),
            'embedding_model': settings.EMBEDDING_MODEL
        }
    }, f, ensure_ascii=False, indent=2)

logger.info(f"✅ Saved to {output_file}")
logger.info(f"📊 Total: {len(verses)} verses with embeddings")

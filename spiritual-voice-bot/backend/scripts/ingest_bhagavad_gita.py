"""
Ingest Bhagavad Gita dataset and create embeddings for RAG pipeline
"""
import os
import sys
import json
import csv
import logging
from pathlib import Path
from typing import List, Dict
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import settings

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False
    logger.warning("sentence-transformers not available. Install with: pip install sentence-transformers")

class BhagavadGitaIngester:
    """Ingest and process Bhagavad Gita dataset"""

    def __init__(self):
        self.raw_data_dir = Path(__file__).parent.parent / "data" / "raw"
        self.processed_data_dir = Path(__file__).parent.parent / "data" / "processed"
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)

        # Initialize embedding model if available
        self.embedding_model = None
        if EMBEDDING_AVAILABLE:
            try:
                logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
                self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")

    def find_dataset_files(self) -> List[Path]:
        """Find all dataset files in raw data directory"""
        files = []

        if not self.raw_data_dir.exists():
            logger.error(f"Raw data directory not found: {self.raw_data_dir}")
            return files

        # Look for CSV files
        csv_files = list(self.raw_data_dir.glob("*.csv"))
        json_files = list(self.raw_data_dir.glob("*.json"))

        files.extend(csv_files)
        files.extend(json_files)

        logger.info(f"Found {len(files)} data files: {[f.name for f in files]}")
        return files

    def parse_csv_file(self, file_path: Path) -> List[Dict]:
        """Parse CSV file and extract verses"""
        verses = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Try to detect delimiter
                sample = f.read(1024)
                f.seek(0)

                # Detect delimiter
                sniffer = csv.Sniffer()
                try:
                    dialect = sniffer.sniff(sample)
                    delimiter = dialect.delimiter
                except:
                    delimiter = ','

                reader = csv.DictReader(f, delimiter=delimiter)

                for row in reader:
                    # Flexible field mapping - adapt to actual dataset structure
                    verse = self._extract_verse_from_row(row)
                    if verse:
                        verses.append(verse)

            logger.info(f"Parsed {len(verses)} verses from {file_path.name}")

        except Exception as e:
            logger.error(f"Error parsing CSV {file_path.name}: {e}")

        return verses

    def parse_json_file(self, file_path: Path) -> List[Dict]:
        """Parse JSON file and extract verses"""
        verses = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle different JSON structures
            if isinstance(data, list):
                for item in data:
                    verse = self._extract_verse_from_dict(item)
                    if verse:
                        verses.append(verse)
            elif isinstance(data, dict):
                # Could be nested structure
                for key, value in data.items():
                    if isinstance(value, list):
                        for item in value:
                            verse = self._extract_verse_from_dict(item)
                            if verse:
                                verses.append(verse)

            logger.info(f"Parsed {len(verses)} verses from {file_path.name}")

        except Exception as e:
            logger.error(f"Error parsing JSON {file_path.name}: {e}")

        return verses

    def _extract_verse_from_row(self, row: Dict) -> Dict:
        """Extract verse information from CSV row (flexible field mapping)"""
        verse = {}

        # Common field names to check (case-insensitive)
        field_mappings = {
            'chapter': ['chapter', 'chapter_num', 'chapter_number', 'adhyaya'],
            'verse': ['verse', 'verse_num', 'verse_number', 'shloka'],
            'text': ['text', 'verse_text', 'translation', 'english', 'english_translation'],
            'sanskrit': ['sanskrit', 'sanskrit_text', 'original', 'devanagari'],
            'transliteration': ['transliteration', 'iast', 'romanized'],
            'meaning': ['meaning', 'explanation', 'commentary', 'description'],
        }

        # Extract fields
        row_lower = {k.lower(): v for k, v in row.items()}

        for field, possible_names in field_mappings.items():
            for name in possible_names:
                if name in row_lower and row_lower[name]:
                    verse[field] = row_lower[name].strip()
                    break

        # Only return if we have at least chapter, verse, and text
        if 'chapter' in verse and 'verse' in verse and 'text' in verse:
            verse['scripture'] = 'Bhagavad Gita'
            verse['reference'] = f"Bhagavad Gita {verse['chapter']}.{verse['verse']}"
            verse['topic'] = self._infer_topic(verse)
            verse['language'] = 'en'  # Assuming English translation

            return verse

        return None

    def _extract_verse_from_dict(self, item: Dict) -> Dict:
        """Extract verse information from dictionary"""
        return self._extract_verse_from_row(item)

    def _infer_topic(self, verse: Dict) -> str:
        """Infer topic from verse content"""
        text = verse.get('text', '').lower()
        meaning = verse.get('meaning', '').lower()
        content = text + ' ' + meaning

        # Topic keywords
        topics = {
            'Karma Yoga': ['action', 'duty', 'work', 'karma', 'perform'],
            'Bhakti Yoga': ['devotion', 'love', 'surrender', 'worship', 'bhakti'],
            'Jnana Yoga': ['knowledge', 'wisdom', 'understand', 'jnana', 'learning'],
            'Mind Control': ['mind', 'control', 'meditation', 'focus', 'discipline'],
            'Soul': ['soul', 'atman', 'self', 'eternal', 'immortal'],
            'Equanimity': ['equal', 'balance', 'neutral', 'steady', 'sama'],
            'Fear': ['fear', 'afraid', 'courage', 'fearless'],
            'Death': ['death', 'mortality', 'rebirth', 'reincarnation'],
            'Liberation': ['liberation', 'moksha', 'freedom', 'enlightenment'],
            'Dharma': ['dharma', 'righteousness', 'duty', 'moral'],
        }

        for topic, keywords in topics.items():
            if any(keyword in content for keyword in keywords):
                return topic

        return 'General Wisdom'

    def generate_embeddings(self, verses: List[Dict]) -> np.ndarray:
        """Generate embeddings for all verses"""
        if not self.embedding_model:
            logger.warning("No embedding model available - using dummy embeddings")
            return np.zeros((len(verses), 768))

        texts = []
        for verse in verses:
            # Combine text and meaning for better semantic representation
            text_parts = [verse.get('text', '')]
            if 'meaning' in verse:
                text_parts.append(verse['meaning'])
            if 'sanskrit' in verse:
                text_parts.append(verse['sanskrit'])

            combined_text = ' '.join(text_parts)
            texts.append(combined_text)

        logger.info(f"Generating embeddings for {len(texts)} verses...")
        embeddings = self.embedding_model.encode(texts, convert_to_tensor=False, show_progress_bar=True)

        logger.info(f"Generated embeddings shape: {embeddings.shape}")
        return embeddings

    def save_processed_data(self, verses: List[Dict], embeddings: np.ndarray):
        """Save processed verses and embeddings"""
        output_file = self.processed_data_dir / "bhagavad_gita_processed.json"

        # Convert embeddings to list for JSON serialization
        for i, verse in enumerate(verses):
            verse['embedding'] = embeddings[i].tolist()

        # Save as JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'verses': verses,
                'metadata': {
                    'total_verses': len(verses),
                    'embedding_dim': len(embeddings[0]) if len(embeddings) > 0 else 0,
                    'embedding_model': settings.EMBEDDING_MODEL,
                    'scripture': 'Bhagavad Gita'
                }
            }, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved processed data to {output_file}")

        # Also save just the verse data without embeddings for easy inspection
        verses_only_file = self.processed_data_dir / "bhagavad_gita_verses.json"
        with open(verses_only_file, 'w', encoding='utf-8') as f:
            verses_copy = [{k: v for k, v in verse.items() if k != 'embedding'} for verse in verses]
            json.dump(verses_copy, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved verses (without embeddings) to {verses_only_file}")

    def ingest_all(self):
        """Main ingestion pipeline"""
        logger.info("=" * 70)
        logger.info("Starting Bhagavad Gita Dataset Ingestion")
        logger.info("=" * 70)

        # Find dataset files
        files = self.find_dataset_files()

        if not files:
            logger.error("\n❌ No dataset files found!")
            logger.error(f"📁 Please download dataset to: {self.raw_data_dir}")
            logger.error("📥 Dataset: https://www.kaggle.com/datasets/a2m2a2n2/bhagwad-gita-dataset")
            logger.error("\nRun: python3 scripts/download_bhagavad_gita.py for instructions")
            return

        # Parse all files
        all_verses = []
        for file_path in files:
            if file_path.suffix == '.csv':
                verses = self.parse_csv_file(file_path)
            elif file_path.suffix == '.json':
                verses = self.parse_json_file(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_path.name}")
                continue

            all_verses.extend(verses)

        if not all_verses:
            logger.error("\n❌ No verses extracted from dataset!")
            return

        logger.info(f"\n✅ Successfully parsed {len(all_verses)} verses")

        # Remove duplicates based on reference
        unique_verses = {}
        for verse in all_verses:
            ref = verse.get('reference')
            if ref not in unique_verses:
                unique_verses[ref] = verse

        all_verses = list(unique_verses.values())
        logger.info(f"✅ {len(all_verses)} unique verses after deduplication")

        # Generate embeddings
        logger.info("\n🔄 Generating embeddings...")
        embeddings = self.generate_embeddings(all_verses)

        # Save processed data
        logger.info("\n💾 Saving processed data...")
        self.save_processed_data(all_verses, embeddings)

        logger.info("\n" + "=" * 70)
        logger.info("✅ Ingestion Complete!")
        logger.info("=" * 70)
        logger.info(f"📊 Total verses processed: {len(all_verses)}")
        logger.info(f"📁 Output directory: {self.processed_data_dir}")
        logger.info(f"📄 Processed data: bhagavad_gita_processed.json")
        logger.info(f"📄 Verses only: bhagavad_gita_verses.json")
        logger.info("\n🚀 Ready to use with RAG pipeline!")

def main():
    """Run ingestion"""
    ingester = BhagavadGitaIngester()
    ingester.ingest_all()

if __name__ == "__main__":
    main()

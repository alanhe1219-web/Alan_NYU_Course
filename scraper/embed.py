import os
import json
import logging
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model to use: Nomic AI Text v1.5
MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"

def load_data(filepath: str):
    logger.info(f"Loading data from {filepath}")
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_embeddings():
    input_file = "scraper/courses_raw.json"
    output_file = "scraper/courses_embedded.json"
    
    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} not found. Please run scrape.py first.")
        return
        
    courses = load_data(input_file)
    if not courses:
        logger.warning("No courses loaded.")
        return
        
    logger.info(f"Loaded {len(courses)} courses. Loading model...")
    # Nomic embed model requires mean pooling (which sentence-transformers handles) and prefix
    # According to Nomic docs: "search_document" is the prefix for general document embedding
    model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)
    
    logger.info(f"Generating embeddings for {len(courses)} courses...")
    
    # Optional: we can combine code, name, and description to give richer semantic context
    textsToEmbed = [
        f"search_document: Course Code: {c['code']} Name: {c.get('name', '')} Subject: {c.get('subject', '')} Description: {c.get('description', '')}"
        for c in courses
    ]
    
    embeddings = model.encode(textsToEmbed, convert_to_tensor=False, show_progress_bar=True)
    
    logger.info("Embeddings generated. Saving to file...")
    for idx, course in enumerate(courses):
        course['embedding'] = embeddings[idx].tolist()
        
    with open(output_file, 'w') as f:
        json.dump(courses, f)
        
    logger.info(f"Saved {len(courses)} embedded courses to {output_file}")

if __name__ == "__main__":
    generate_embeddings()

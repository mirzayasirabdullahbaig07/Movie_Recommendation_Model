import os
import joblib
import gdown
import logging

# ----------------------------
# Setup logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("recommend.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# ----------------------------
# Download function
# ----------------------------
def download_from_drive(file_id, filename):
    """Download file from Google Drive if it does not exist locally."""
    if not os.path.exists(filename):
        url = f"https://drive.google.com/uc?id={file_id}"
        logging.info(f"⬇️ Downloading {filename} from Google Drive...")
        gdown.download(url, filename, quiet=False, fuzzy=True)
    else:
        logging.info(f"✅ {filename} already exists locally.")

# ----------------------------
# Google Drive File ID
# ----------------------------
COSINE_FILE_ID = "1YWaK7bi9D-CRMS1tclLj_0h4J5s77hM6"
COSINE_FILE = "cosine_sim.pkl"

# ----------------------------
# Download files if missing
# ----------------------------
download_from_drive(COSINE_FILE_ID, COSINE_FILE)

# ----------------------------
# Load data
# ----------------------------
try:
    logging.info("🔁 Loading data...")
    df = joblib.load('df_cleaned.pkl')  # Make sure this is in your repo
    cosine_sim = joblib.load(COSINE_FILE)
    logging.info("✅ Data loaded successfully.")
except Exception as e:
    logging.error("❌ Failed to load required files: %s", str(e))
    raise e

# ----------------------------
# Movie recommendation function
# ----------------------------
def recommend_movies(movie_name, top_n=5):
    logging.info("🎬 Recommending movies for: '%s'", movie_name)
    idx = df[df['title'].str.lower() == movie_name.lower()].index
    if len(idx) == 0:
        logging.warning("⚠️ Movie not found in dataset.")
        return None
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    logging.info("✅ Top %d recommendations ready.", top_n)

    # Create DataFrame with clean serial numbers starting from 1
    result_df = df[['title']].iloc[movie_indices].reset_index(drop=True)
    result_df.index = result_df.index + 1  # Start from 1 instead of 0
    result_df.index.name = "S.No."
    return result_df

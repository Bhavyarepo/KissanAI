import os
import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from kaggle_manager import KaggleDatasetManager, ensure_dir

DATASET_SLUGS = [
    "arjunyadav99/indian-agricultural-mandi-prices-20232025",
    "zoya77/simulated-crop-price-with-economic-indicators-data",
    "varshitanalluri/crop-price-prediction-dataset",
    "anshtanwar/current-daily-price-of-various-commodities-india"
]

def load_any_csvs(base_dir: str, subdir: str):
    folder = os.path.join(base_dir, subdir)
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith('.csv'):
                path = os.path.join(root, f)
                try:
                    df = pd.read_csv(path)
                    if len(df) > 10:
                        yield df
                except Exception:
                    continue

def main():
    datasets_root = os.getenv('DATASETS_DIR', 'datasets')
    models_root = os.getenv('MODELS_DIR', 'models')
    ensure_dir(datasets_root)
    ensure_dir(models_root)

    kdm = KaggleDatasetManager(datasets_root)
    frames = []
    for slug in DATASET_SLUGS:
        sub = slug.split('/')[-1]
        kdm.download_if_missing(slug, sub)
        frames.extend(list(load_any_csvs(datasets_root, sub)))
    if not frames:
        raise RuntimeError("No price dataset CSV loaded")
    df = pd.concat(frames, ignore_index=True, sort=False)
    df.columns = [c.strip().lower() for c in df.columns]

    # Heuristic: look for columns containing 'price'
    price_cols = [c for c in df.columns if 'price' in c]
    if not price_cols:
        raise RuntimeError("No price column found")
    y_col = price_cols[0]

    # Numeric features only for baseline
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if y_col not in numeric_cols:
        # Try to coerce
        df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    features = [c for c in numeric_cols if c != y_col]
    X = df[features].fillna(df[features].median())
    y = df[y_col].fillna(df[y_col].median())

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBRegressor(n_estimators=500, max_depth=6, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9)
    model.fit(Xtr, ytr)
    mae = mean_absolute_error(yte, model.predict(Xte))
    print(f"Price model MAE: {mae:.3f}")

    joblib.dump(model, os.path.join(models_root, 'price_model.pkl'))

if __name__ == '__main__':
    main()







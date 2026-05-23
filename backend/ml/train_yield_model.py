import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from pathlib import Path
from kaggle_manager import KaggleDatasetManager, ensure_dir

DATASET_SLUGS = [
    "aaryanmavaninew/hyperparameter-tuned-crop-yield-ml-dataset",
    "vedikasd/crop-data-for-yield-and-recommendation-analysis",
]

def load_any_csv(base_dir: str, subdir: str) -> pd.DataFrame:
    folder = os.path.join(base_dir, subdir)
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith('.csv'):
                try:
                    return pd.read_csv(os.path.join(root, f))
                except Exception:
                    continue
    raise RuntimeError(f"No CSV found under {subdir}")

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
        try:
            frames.append(load_any_csv(datasets_root, sub))
        except Exception:
            pass
    if not frames:
        raise RuntimeError("No yield dataset CSV loaded")
    df = pd.concat(frames, ignore_index=True)
    df.columns = [c.strip().lower() for c in df.columns]

    # Heuristic select features
    y_col = None
    for cand in ['yield', 'yield_kg', 'yield_kg_per_ha', 'production', 'yield_ton_ha']:
        if cand in df.columns:
            y_col = cand
            break
    if y_col is None:
        raise RuntimeError("Yield target column not found")

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if y_col not in numeric_cols:
        raise RuntimeError("Yield column not numeric")
    features = [c for c in numeric_cols if c != y_col]
    X = df[features].fillna(df[features].median())
    y = df[y_col].fillna(df[y_col].median())

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9)
    model.fit(Xtr, ytr)
    r2 = r2_score(yte, model.predict(Xte))
    print(f"Yield model R2: {r2:.3f}")

    joblib.dump(model, os.path.join(models_root, 'yield_model.pkl'))

if __name__ == '__main__':
    main()







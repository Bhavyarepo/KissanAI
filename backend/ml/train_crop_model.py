import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
from xgboost import XGBClassifier
from pathlib import Path
from kaggle_manager import KaggleDatasetManager, ensure_dir

DATASET_SLUGS = [
    "madhuraatmarambhagat/crop-recommendation-dataset",
    "raghavdharwal/crop-recommendation-dataset-field-crop-varieties",
]

def load_datasets(base_dir: str) -> pd.DataFrame:
    frames = []
    for slug in DATASET_SLUGS:
        subdir = slug.split('/')[-1]
        local = os.path.join(base_dir, subdir)
        # Attempt common file names
        for fname in [
            'Crop_recommendation.csv', 'crop_recommendation.csv',
            'Crop_recommendation - Sheet1.csv', 'data.csv'
        ]:
            fpath = os.path.join(local, fname)
            if os.path.exists(fpath):
                frames.append(pd.read_csv(fpath))
                break
    if not frames:
        raise RuntimeError("No crop recommendation CSV found in downloaded datasets.")
    return pd.concat(frames, ignore_index=True)

def main():
    datasets_root = os.getenv('DATASETS_DIR', 'datasets')
    models_root = os.getenv('MODELS_DIR', 'models')
    ensure_dir(datasets_root)
    ensure_dir(models_root)

    kdm = KaggleDatasetManager(datasets_root)
    for slug in DATASET_SLUGS:
        kdm.download_if_missing(slug, slug.split('/')[-1])

    df = load_datasets(datasets_root)
    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    # Expect features: N, P, K, temperature, humidity, ph, rainfall; target: label
    feature_candidates = ['n','p','k','temperature','humidity','ph','rainfall']
    features = [c for c in feature_candidates if c in df.columns]
    target = 'label' if 'label' in df.columns else 'crop'
    X = df[features]
    y = df[target]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    Xtr, Xte, ytr, yte = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    model = XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9, eval_metric='mlogloss')
    model.fit(Xtr, ytr)
    preds = model.predict(Xte)
    f1 = f1_score(yte, preds, average='weighted')
    print(f"Crop model F1-weighted: {f1:.3f}")

    # Save
    joblib.dump(model, os.path.join(models_root, 'crop_model.pkl'))
    joblib.dump(scaler, os.path.join(models_root, 'scaler.pkl'))

if __name__ == '__main__':
    main()







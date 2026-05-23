import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
from xgboost import XGBClassifier
from kaggle_manager import KaggleDatasetManager, ensure_dir

DATASET_SLUGS = [
    "marwanmostafa16/fertilizer-prediction",
    "irakozekelly/fertilizer-prediction",
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
        raise RuntimeError("No fertilizer dataset CSV loaded")
    df = pd.concat(frames, ignore_index=True)
    df.columns = [c.strip().lower() for c in df.columns]

    target = None
    for cand in ['fertilizer', 'fertilizer_name', 'label']:
        if cand in df.columns:
            target = cand
            break
    if target is None:
        raise RuntimeError("Fertilizer target not found")

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    X = df[numeric_cols].copy().fillna(df[numeric_cols].median())
    y = df[target].astype(str)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=0.2, random_state=42, stratify=y)
    model = XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9, eval_metric='mlogloss')
    model.fit(Xtr, ytr)
    f1 = f1_score(yte, model.predict(Xte), average='weighted')
    print(f"Fertilizer model F1: {f1:.3f}")

    joblib.dump(model, os.path.join(models_root, 'fertilizer_model.pkl'))
    joblib.dump(scaler, os.path.join(models_root, 'fertilizer_scaler.pkl'))

if __name__ == '__main__':
    main()







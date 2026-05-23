import os
import json
from pathlib import Path
import pandas as pd
from datasets import Dataset
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification, Trainer, TrainingArguments
import tensorflow as tf
from kaggle_manager import KaggleDatasetManager, ensure_dir

DATASET_SLUG = "viswaprakash1990/farming-faq-assistant-dataset"

def main():
    datasets_root = os.getenv('DATASETS_DIR', 'datasets')
    models_root = os.getenv('MODELS_DIR', 'models')
    ensure_dir(datasets_root)
    ensure_dir(models_root)

    kdm = KaggleDatasetManager(datasets_root)
    sub = DATASET_SLUG.split('/')[-1]
    local = kdm.download_if_missing(DATASET_SLUG, sub)

    # Attempt to locate a CSV of FAQs
    df = None
    for root, _, files in os.walk(local):
        for f in files:
            if f.lower().endswith('.csv'):
                try:
                    df = pd.read_csv(os.path.join(root, f))
                    if 'question' in df.columns and 'answer' in df.columns:
                        break
                except Exception:
                    continue
        if df is not None:
            break
    if df is None:
        raise RuntimeError("FAQ dataset not found or doesn't have question/answer")

    # Build simple pair classification: question->answer category; for baseline use sequence pair classification as concatenated text
    df = df.dropna(subset=['question','answer']).sample(frac=1.0, random_state=42).reset_index(drop=True)
    # For baseline, we'll train a classifier to predict if a retrieved answer matches question (positive), with negatives sampled
    # Create pairs
    positives = pd.DataFrame({
        'text': df['question'] + ' [SEP] ' + df['answer'],
        'label': 1
    })
    # Negatives by shuffling answers
    negatives = df.copy()
    negatives['answer'] = negatives['answer'].sample(frac=1.0, random_state=0).values
    negatives = pd.DataFrame({
        'text': negatives['question'] + ' [SEP] ' + negatives['answer'],
        'label': 0
    })
    pairs = pd.concat([positives, negatives], ignore_index=True).sample(frac=1.0, random_state=1).reset_index(drop=True)

    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    encodings = tokenizer(list(pairs['text'].values), truncation=True, padding=True)
    labels = pairs['label'].values
    ds = tf.data.Dataset.from_tensor_slices((dict(encodings), labels)).batch(16)

    model = TFDistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
    optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    model.fit(ds, epochs=2)

    model.save_pretrained(os.path.join(models_root, 'faq_model'))
    tokenizer.save_pretrained(os.path.join(models_root, 'faq_model'))

if __name__ == '__main__':
    main()







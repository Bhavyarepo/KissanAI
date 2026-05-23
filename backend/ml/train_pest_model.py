import os
import tensorflow as tf
from tensorflow.keras import layers, models
from kaggle_manager import KaggleDatasetManager, ensure_dir

# There isn't a single canonical pest dataset in the list; reuse disease datasets as placeholder or expect a 'pests' folder if provided
DATASET_SLUGS = [
    "karagwaanntreasure/plant-disease-detection",
]

def build_model(num_classes: int):
    model = models.Sequential([
        layers.Input(shape=(224,224,3)),
        layers.Rescaling(1./255),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, activation='relu'),
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def main():
    datasets_root = os.getenv('DATASETS_DIR', 'datasets')
    models_root = os.getenv('MODELS_DIR', 'models')
    ensure_dir(datasets_root)
    ensure_dir(models_root)

    kdm = KaggleDatasetManager(datasets_root)
    for slug in DATASET_SLUGS:
        kdm.download_if_missing(slug, slug.split('/')[-1])

    dataset_dir = os.path.join(datasets_root, 'pests')
    if not os.path.exists(dataset_dir):
        # fallback to any dataset dir; users can replace with real pest dataset structure
        dataset_dir = os.path.join(datasets_root, DATASET_SLUGS[0].split('/')[-1])

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=(224,224),
        batch_size=32,
        shuffle=True
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=(224,224),
        batch_size=32,
        shuffle=True
    )
    num_classes = len(train_ds.class_names)
    model = build_model(num_classes)
    model.fit(train_ds, validation_data=val_ds, epochs=5)
    model.save(os.path.join(models_root, 'pest_model.h5'))

if __name__ == '__main__':
    main()







import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from imutils import paths
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import AveragePooling2D, Dropout, Flatten, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
import os

# --- CONFIGURATION ---
# UPDATE THIS PATH to match the folder name you uploaded
# For example, if your folder is named 'dataset', change this to 'dataset'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = r"C:\Users\chopr\Downloads\Parkinson-Project-main\Parkinson-Project-main\dataset"

INIT_LR = 1e-3  # Increased for better convergence
EPOCHS = 100  # Full training for reliable model
BS = 16  # Increased batch size for more stable gradients


def load_data(dataset_path):
    print(f"[INFO] loading images from {dataset_path}...")
    imagePaths = list(paths.list_images(dataset_path))
    data = []
    labels = []

    if not imagePaths:
        raise ValueError(f"No images found in '{dataset_path}'. Please check your folder structure.")

    for imagePath in imagePaths:
        # Extract the class label from the filename
        label = imagePath.split(os.path.sep)[-2]

        # Load the image, swap color channels, and resize it to 224x224
        image = cv2.imread(imagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))

        data.append(image)
        labels.append(label)

    # Convert to NumPy arrays and scale pixel intensities to [0, 1]
    data = np.array(data) / 255.0
    labels = np.array(labels)

    return data, labels


def build_model():
    print("[INFO] compiling model...")
    # Load VGG16 network
    baseModel = VGG16(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))

    # Construct a slightly stronger head
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(128, activation="relu")(headModel)  # Increased from 64 to 128
    headModel = Dropout(0.4)(headModel)                   # Sightly lower dropout to prevent underfitting
    headModel = Dense(2, activation="softmax")(headModel)

    model = Model(inputs=baseModel.input, outputs=headModel)

    # --- FINE-TUNING STRATEGY ---
    # Instead of freezing everything, unfreeze the last convolutional block (Block 5)
    # This allows the model to learn abstract handwriting features.
    for layer in baseModel.layers:
        if layer.name.startswith("block5_"):
            layer.trainable = True
        else:
            layer.trainable = False

    # Use reasonable learning rate for fine-tuning
    opt = Adam(learning_rate=1e-4) 
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    return model

def plot_history(H, epochs):
    print("[INFO] plotting training history...")
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, epochs), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epochs), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, epochs), H.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, epochs), H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig("plot.png")  # Saves the plot to your project folder
    plt.show()  # Opens a window with the graph


if __name__ == "__main__":
    # 1. Load Data
    try:
        data, labels = load_data(DATASET_PATH)
    except Exception as e:
        print(e)
        exit()

    # 2. Encode Labels
    lb = LabelEncoder()
    labels = lb.fit_transform(labels)
    labels = to_categorical(labels)

    # 3. Split Data
    (trainX, testX, trainY, testY) = train_test_split(data, labels,
                                                      test_size=0.20, stratify=labels, random_state=42)

    # 4. Data Augmentation
    aug = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest")

    # 5. Build and Train Model
    model = build_model()

    print("[INFO] training head...")
    H = model.fit(
        aug.flow(trainX, trainY, batch_size=BS),
        validation_data=(testX, testY),
        epochs=EPOCHS)

    # 6. Evaluate
    print("[INFO] evaluating network...")
    predIdxs = model.predict(testX, batch_size=BS)
    predIdxs = np.argmax(predIdxs, axis=1)
    
    # Print detailed evaluation metrics
    print("\n" + "="*50)
    print("[METRICS] Model Evaluation:")
    print(f"Test Accuracy: {np.mean(predIdxs == testY.argmax(axis=1)):.4f}")
    print("\nClassification Report:")
    print(classification_report(testY.argmax(axis=1), predIdxs, target_names=lb.classes_))
    print("\nConfusion Matrix:")
    print(confusion_matrix(testY.argmax(axis=1), predIdxs))
    print("="*50 + "\n")

    # 7. Save Model
    print("[INFO] saving model...")
    model_path = os.path.join(BASE_DIR, "model", "parkinsons_detector.keras")
    model.save(model_path)
    print(f"[INFO] Model saved to {model_path}")

    print("[SUCCESS] Training complete!")
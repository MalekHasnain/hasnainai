# Verify VGG16 page code blocks compile (syntax check only, TF not needed locally)
import py_compile, tempfile, textwrap, sys

blocks = []
blocks.append('''# TensorFlow's Keras API: model building, layers, and the VGG16 model itself
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras import layers, models
# Pre-trained VGG16 weights are downloaded from a public Keras mirror (no login needed)
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report''')

blocks.append('''# CIFAR-10 ships inside Keras, so one call downloads the ready-made train/test split
# (same dataset as Topic 02: 60000 32x32 colour images, 10 classes)
from tensorflow.keras.datasets import cifar10
(X_train_full, y_train_full), (X_test_full, y_test_full) = cifar10.load_data()

# Free Colab is slow, so keep only a subset: first 5000 train / 1000 test images
# Classes are already shuffled, so a slice keeps all 10 labels balanced enough
X_train_raw, y_train = X_train_full[:5000], y_train_full[:5000]
X_test_raw,  y_test  = X_test_full[:1000],  y_test_full[:1000]

# Labels come as a column vector -> flatten to a 1-D array of class ids 0..9
y_train, y_test = y_train.ravel(), y_test.ravel()

# The 10 class names, in label order (airplane=0 ... truck=9)
class_names = ["airplane","automobile","bird","cat","deer",
               "dog","frog","horse","ship","truck"]
print("Train subset:", X_train_raw.shape, "Test subset:", X_test_raw.shape)''')

blocks.append('''# VGG16 refuses inputs smaller than 32x32; we upscale 32->48 so early pooling
# still leaves enough pixels for the deep stack of convolutions
X_train = tf.image.resize(X_train_raw, (48, 48)).numpy()
X_test  = tf.image.resize(X_test_raw,  (48, 48)).numpy()

# VGG16-specific preprocessing: RGB->BGR then zero-centre each channel
# using the ImageNet means the pre-trained weights were trained with
X_train = preprocess_input(X_train)
X_test  = preprocess_input(X_test)
print("After resize + preprocess:", X_train.shape, X_test.shape)''')

blocks.append('''# Load VGG16 WITHOUT its 1000-class ImageNet head but WITH learned ImageNet weights
# weights="imagenet" is the transfer-learning switch: it loads the filters the
# Oxford group learned from 1.4M images instead of starting from random numbers
base = VGG16(weights="imagenet", include_top=False, input_shape=(48, 48, 3))

# Freeze the base: set every weight to non-trainable
# Why: with only 5000 images we would overwrite (destroy) the general ImageNet
# features if our small dataset pushed big gradient updates into the base
base.trainable = False
base.summary()''')

blocks.append('''# Build a small "head": our own classifier that sits on top of the frozen base
model = models.Sequential([
    base,                                        # frozen VGG16 feature extractor
    layers.GlobalAveragePooling2D(),             # average each 3x3x512 feature map -> 512 numbers
    layers.Dense(128, activation="relu"),        # small fully-connected layer to recombine features
    layers.Dropout(0.3),                         # randomly zero 30% of activations to fight overfitting
    layers.Dense(10, activation="softmax")       # 10 outputs = CIFAR-10 class probabilities
])
model.summary()''')

blocks.append('''# Compile: adam optimizer, sparse categorical cross-entropy (labels are ints, not one-hot)
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# Train only the ~170k head weights (the 14.7M base weights stay frozen)
# 3 epochs x 125 steps keeps the run under ~10 minutes on a free Colab GPU
history = model.fit(X_train, y_train,
                    epochs=3,
                    batch_size=40,
                    validation_split=0.15,
                    verbose=1)''')

blocks.append('''# Evaluate on the held-out 1000 test images
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_acc:.3f}")

# Confusion matrix (Topic 01): which classes get confused with which
y_pred = model.predict(X_test, verbose=0).argmax(axis=1)   # argmax picks the top class
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=class_names)
fig, ax = plt.subplots(figsize=(9, 9))
disp.plot(ax=ax, xticks_rotation=45, cmap="Blues", colorbar=False)
plt.title("VGG16 transfer learning - CIFAR-10 (subset)")
plt.tight_layout()
plt.show()

# Per-class precision / recall / F1 to spot weak classes
print(classification_report(y_test, y_pred, target_names=class_names))''')

blocks.append('''# Pick one test image and predict it, showing the model's confidence
i = 12
prob = model.predict(X_test[i:i+1], verbose=0)[0]     # softmax over 10 classes
rank = prob.argsort()[::-1]                           # class ids sorted best to worst

plt.imshow(X_test_raw[i])
plt.title(f"True: {class_names[y_test[i]]}")
plt.axis("off")
plt.show()

for c in rank[:3]:
    print(f"{class_names[c]:12s} {prob[c]*100:5.1f}%")''')

blocks.append('''# Feature extraction mode: throw away the head, keep the 512-dim VGG16 embedding
# These vectors are reusable input for OTHER algorithms (SVM, K-Means, PCA)
features = base.predict(X_test[:500], verbose=0)
print("Embedding shape:", features.shape)   # (500, 3, 3, 512) before pooling
flat = features.reshape(features.shape[0], -1)
print("Flattened for SVM / K-Means:", flat.shape)   # (500, 4608)''')

ok = True
for n, b in enumerate(blocks, 1):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(b)
        path = f.name
    try:
        py_compile.compile(path, doraise=True)
        print(f"Block {n}: OK")
    except py_compile.PyCompileError as e:
        ok = False
        print(f"Block {n}: FAIL\n{e}")
sys.exit(0 if ok else 1)

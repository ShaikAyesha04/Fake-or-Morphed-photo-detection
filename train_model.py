import os
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import ResNet50  # Importing ResNet50
from tensorflow.keras.callbacks import ModelCheckpoint


# Constants for paths and image dimensions
TRAIN_DIR = 'dataset'  # Replace with your train dataset path
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 8
EPOCHS =10

# ImageDataGenerator with validation split
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2  # Split 20% of data for validation
)

# Prepare the data generators
train_data = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'  # Use as training data
)

val_data = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'  # Use as validation data
)

# Build the model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))
base_model.trainable = False  # Freeze base layers initially

# Add custom layers on top of ResNet50 base model
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dense(3, activation='softmax')  # 3 classes: Real, Fake, Morphed
])

# Compile the model (initially only training the custom layers)
model.compile(optimizer=Adam(learning_rate=0.0001), 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

# Set up callbacks: EarlyStopping and ModelCheckpoint
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, save_weights_only=True)
checkpoint_callback = ModelCheckpoint(
    filepath='best_model.h5',    # Save the model to this file
    monitor='val_accuracy',      # You can also use 'accuracy' if you have no validation
    save_best_only=True,         # Only saves if model improves
    save_weights_only=False,     # Saves full model
    verbose=1
)

# Train the model with frozen layers
history = model.fit(
    train_data,
    epochs=EPOCHS,
    validation_data=val_data,
    callbacks=[early_stopping, model_checkpoint],
    verbose=1
    history = model.fit(
    train_generator,
    epochs=EPOCHS,
    callbacks=[checkpoint_callback],   # <<< add this line
    steps_per_epoch=train_generator.samples // train_generator.batch_size
)

)

# Unfreeze some layers for fine-tuning after initial training
base_model.trainable = True

# Freeze earlier layers and unfreeze deeper ones (for fine-tuning)
for layer in base_model.layers[:140]:  # Freeze the first 140 layers
    layer.trainable = False

# Recompile the model with a smaller learning rate for fine-tuning
model.compile(optimizer=Adam(learning_rate=0.00001),  # Reduce learning rate for fine-tuning
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Continue training with fine-tuning
history_fine_tune = model.fit(
    train_data,
    epochs=EPOCHS,  # Continue training for additional epochs
    validation_data=val_data,
    callbacks=[early_stopping, model_checkpoint],
    verbose=1
)
# Inside your epoch loop:
for epoch in range(start_epoch, num_epochs):
    # Your training code...

    # Check if user asked to save manually
    if os.path.exists("save_now.txt"):
        torch.save(model.state_dict(), f"checkpoint_manual_epoch_{epoch}.pt")
        print(f"Manual checkpoint saved at epoch {epoch}!")
        os.remove("save_now.txt")  # Remove the trigger file

# Save final model after fine-tuning
model.save('final_fine_tuned_model.h5')


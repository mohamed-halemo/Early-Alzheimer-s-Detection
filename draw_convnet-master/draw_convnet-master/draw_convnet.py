import matplotlib.pyplot as plt
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from matplotlib.patches import Rectangle, Circle
#commment it and don't run it when you load model 
from tensorflow.keras.applications import VGG16,VGG19,ResNet50
import numpy as np
from tensorflow.keras.models import Model


input_shape=[150,150,3]
# Load the pretrained VGG16 model
base_model=VGG16(weights='imagenet', include_top=False, input_shape=input_shape)

# Freeze the layers of the pretrained model
for layer in base_model.layers[:-15]:
   layer.trainable = False
    #freeze all layers
# for layer in base_model.layers:
#     layer.trainable = False

# Add new classification layers on top of the base model
x = Flatten()(base_model.output)
x = Dense(1024, activation='relu')(x)
# x = Dropout(0.5)(x)  # Add dropout with a rate of 
x = Dense(512, activation='relu')(x)
# x = Dropout(0.5)(x)  # Add dropout with a rate of 
# x = Dense(256, activation='relu')(x)
# x = Dropout(0.5)(x)  # Add dropout with a rate of 
# # x = Dense(128, activation='relu',kernel_regularizer='l2')(x)

# x = Dense(128, activation='relu')(x)
# x = Dropout(0.5)(x)  # Add dropout with a rate of 

# x = Dense(64, activation='relu', kernel_regularizer='l2')(x)
# x = Dropout(0.5)(x)  # Add dropout with a rate of 

# x = Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.01))(x)

output = Dense(3, activation='softmax')(x)

# Create the model
model = Model(inputs=base_model.input, outputs=output)

# Print the model summary
model.summary()
patches = []
colors = []
layer_sizes = []
current_loc = [0, 0]

# Helper function to add a layer to the visualization
def add_layer(layer_type, layer_size):
    global current_loc
    if layer_type == 'Conv2D':
        patches.append(Rectangle(current_loc, 1, layer_size))
    elif layer_type == 'MaxPooling2D':
        patches.append(Rectangle(current_loc, 0.5, layer_size))
    elif layer_type == 'Flatten':
        patches.append(Rectangle(current_loc, 0.2, layer_size))
    elif layer_type == 'Dense':
        patches.append(Rectangle(current_loc, -1, layer_size))
    colors.append(np.random.rand(3))
    current_loc[0] += 1
    layer_sizes.append(layer_size)

# Visualize the model architecture
for layer in model.layers:
    if isinstance(layer, Conv2D):
        add_layer('Conv2D', layer.filters)
    elif isinstance(layer, MaxPooling2D):
        add_layer('MaxPooling2D', layer.pool_size[0])
    elif isinstance(layer, Flatten):
        add_layer('Flatten', layer_sizes[-1])
    elif isinstance(layer, Dense):
        add_layer('Dense', layer.units)

# Plot the architecture visualization
fig, ax = plt.subplots(figsize=(10, 6))
for i, patch in enumerate(patches):
    patch.set_color(colors[i])
    ax.add_patch(patch)
    x = patch.get_x()
    y = patch.get_y() + patch.get_height() / 2
    ax.annotate(layer_sizes[i], (x, y), color='white', weight='bold',
                ha='center', va='center', fontsize=8)

ax.set_xlim([-0.5, current_loc[0] + 0.5])
ax.set_ylim([0, max(layer_sizes)])
ax.axis('off')
plt.show()
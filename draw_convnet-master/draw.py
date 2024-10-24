import visualkeras
import tensorflow as tf
import os
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Conv2D,Flatten,Dense,PReLU,BatchNormalization,GlobalAveragePooling2D,GlobalAvgPool2D,InputLayer,MaxPooling2D,Dropout

from tensorflow.keras.applications import VGG16,VGG19,ResNet50

from tensorflow.keras.models import Model
from PIL import ImageFont
from tensorflow.python.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, ZeroPadding2D
from collections import defaultdict

color_map = defaultdict(dict)
color_map[Conv2D]['fill'] = '#89CFF0'
color_map[ZeroPadding2D]['fill'] = 'gray'
color_map[Dropout]['fill'] = 'red'
color_map[MaxPooling2D]['fill'] = 'pink'
color_map[Dense]['fill'] = '#D3D3D3'
color_map[Flatten]['fill'] = '#3EB489'


input_shape=[150,150,3]
# Load the pretrained VGG16 model
base_model=VGG16(weights='imagenet', include_top=False, input_shape=input_shape)

# Freeze the layers of the pretrained model
for layer in base_model.layers[:-15]:
   layer.trainable = False

# Add new classification layers on top of the base model
x = Flatten()(base_model.output)
x = Dense(1024, activation='relu')(x)
x = Dense(512, activation='relu')(x)

output = Dense(3, activation='softmax')(x)

# Create the model
model = Model(inputs=base_model.input, outputs=output)

font = ImageFont.truetype("arial.ttf", 32)  # using comic sans is strictly prohibited!
visualkeras.layered_view(model, legend=True, font=font, color_map=color_map,spacing=50)  # font is optional!
# Print the model summary
visualkeras.layered_view(model, legend=True, font=font, color_map=color_map,spacing=50).show() # display using your system viewer
visualkeras.layered_view(model, to_file='output.png', legend=True, font=font, color_map=color_map,spacing=50) # write to disk
visualkeras.layered_view(model, to_file='output.png', legend=True, font=font, color_map=color_map,spacing=50).show() # write and show
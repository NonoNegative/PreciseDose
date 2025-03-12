#    This file was created by
#    MATLAB Deep Learning Toolbox Converter for TensorFlow Models.
#    12-Mar-2025 21:59:37

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def create_model():
    input = keras.Input(shape=(7,))
    fc_1 = layers.Dense(256, name="fc_1_")(input)
    batchnorm_1 = layers.BatchNormalization(epsilon=0.000010, name="batchnorm_1_")(fc_1)
    relu_1 = layers.ReLU()(batchnorm_1)
    fc_2 = layers.Dense(512, name="fc_2_")(relu_1)
    batchnorm_2 = layers.BatchNormalization(epsilon=0.000010, name="batchnorm_2_")(fc_2)
    relu_2 = layers.ReLU()(batchnorm_2)
    dropout_1 = layers.Dropout(0.300000)(relu_2)
    fc_3 = layers.Dense(256, name="fc_3_")(dropout_1)
    batchnorm_3 = layers.BatchNormalization(epsilon=0.000010, name="batchnorm_3_")(fc_3)
    relu_3 = layers.ReLU()(batchnorm_3)
    dropout_2 = layers.Dropout(0.100000)(relu_3)
    fc_4 = layers.Dense(128, name="fc_4_")(dropout_2)
    batchnorm_4 = layers.BatchNormalization(epsilon=0.000010, name="batchnorm_4_")(fc_4)
    relu_4 = layers.ReLU()(batchnorm_4)
    fc_5 = layers.Dense(1, name="fc_5_")(relu_4)

    model = keras.Model(inputs=[input], outputs=[fc_5])
    return model

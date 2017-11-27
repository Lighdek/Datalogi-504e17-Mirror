import tensorflow as tf
from . import Layers
from . import ActivationFunctions

stride = [1, 1, 1, 1]  # input shape.
stddev = 0.5

# pool
pool_k_size = [1, 2, 2, 1]
image_size = 28
pool_stride = [1, 2, 2, 1]


def init_model(input_tensor):

    # 1
    layer1_conv = Layers.conv_layer(input_tensor=input_tensor, input_depth=3, filter_size=5,
                                                   output_depth=6, name="conv1", strides=stride, stddev=stddev)
    layer1_pool = Layers.max_pooling_layer(input_tensor=layer1_conv, name="pool1", stride=pool_stride,
                                           ksize=pool_k_size)
    layer1_relu = ActivationFunctions.relu_layer(input_=layer1_pool, name="relu1")

    # 2
    layer2_conv = Layers.conv_layer(input_tensor=layer1_relu, input_depth=6, filter_size=5,
                                    output_depth=16, name="conv2", strides=stride, stddev=stddev)
    layer2_pool = Layers.max_pooling_layer(input_tensor=layer2_conv, name="pool2", stride=pool_stride,
                                           ksize=pool_k_size)
    layer2_relu = ActivationFunctions.relu_layer(input_=layer2_pool,
                                                 name="relu2")
    # -----------------------------------------------------------------------------------

    # Flatten Layer
    num_features = layer2_relu.get_shape()[1:4].num_elements()
    layer_flat = tf.reshape(layer2_relu, [-1, num_features])# -1 finds size on run time

    # Fully-Connected Layer 1
    layer_fc1 = Layers.fully_connected_layer(input_tensor=layer_flat,
                                             num_of_input=num_features,
                                             num_of_outputs=128,
                                             name="fc1",
                                             distribution=stddev)

    # RelU layer 3
    layer_relu3 = ActivationFunctions.relu_layer(layer_fc1, name="relu3")

    # Fully-Connected Layer 2
    layer_fc2 = Layers.fully_connected_layer(input_tensor=layer_relu3,
                                             num_of_input=128,
                                             num_of_outputs=2,
                                             name="fc2",
                                             distribution=stddev)
    return layer_fc2


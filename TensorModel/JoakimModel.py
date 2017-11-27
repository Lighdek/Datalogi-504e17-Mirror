import tensorflow as flow
import LayerFunctions as layer
import activationfunctions as actiavation

def init_model(x_image, conf):

    # Convolutional Layer 1
    layer_conv1, weights_conv1 = layer.conv_layer(input_=x_image,
                                                  num_of_inputs=3,
                                                  filter_size=5,
                                                  num_of_filters=6,
                                                  name="conv1",
                                                  stride=conf.stride,
                                                  distribution=conf.dist)

    # Pooling Layer 1
    layer_pool1 = layer.max_pooling_layer(input_=layer_conv1,
                                          name="pool1",
                                          stride=conf.pool_stride,
                                          ksize=conf.k_size)

    # RelU layer 1
    layer_relu1 = actiavation.relu_layer(input_=layer_pool1,
                                         name="relu1")

    # -----------------------------------------------------------------------------------

    # Convolutional Layer 2
    layer_conv2, weights_conv2 = layer.conv_layer(input_=layer_relu1,
                                                  num_of_inputs=6,
                                                  filter_size=5,
                                                  num_of_filters=16,
                                                  name="conv2",
                                                  stride=conf.stride,
                                                  distribution=conf.dist)

    # Pooling Layer 2
    layer_pool2 = layer.max_pooling_layer(input_=layer_conv2,
                                          name="pool2",
                                          stride=conf.pool_stride,
                                          ksize=conf.k_size)

    # RelU layer 2
    layer_relu2 = actiavation.relu_layer(input_=layer_pool2,
                                          name="relu2")
    # -----------------------------------------------------------------------------------

    # Flatten Layer
    num_features = layer_relu2.get_shape()[1:4].num_elements()
    layer_flat = flow.reshape(layer_relu2, [-1, num_features])# -1 finds size on run time

    # Fully-Connected Layer 1
    layer_fc1 = layer.fully_connected_layer(input_=layer_flat,
                                            num_of_input=num_features,
                                            num_of_outputs=128,
                                            name="fc1",
                                            distribution=conf.dist)

    # RelU layer 3
    layer_relu3 = actiavation.relu_layer(layer_fc1, name="relu3")

    # Fully-Connected Layer 2
    layer_fc2 = layer.fully_connected_layer(input_=layer_relu3,
                                            num_of_input=128,
                                            num_of_outputs=2,
                                            name="fc2",
                                            distribution=conf.dist)
    return layer_fc2


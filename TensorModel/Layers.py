import tensorflow as tf

def conv_layer(input_tensor, input_depth, filter_size, output_depth, name, strides, stddev):

    with tf.variable_scope(name) as block:
        matrix_shape = [filter_size, filter_size, input_depth, output_depth]

        kernels = tf.Variable(tf.truncated_normal(matrix_shape, stddev=stddev), name="kernels")
        biases = tf.Variable(tf.constant(0.05, shape=(output_depth,)), name="biases")

        layer_tensor = tf.nn.conv2d(input=input_tensor, filter=kernels, strides=strides, padding='VALID') + biases

        return layer_tensor


def fully_connected_layer(input_tensor, num_of_input, num_of_outputs, name, distribution):

    with tf.variable_scope(name) as scope:
        weights = tf.Variable(tf.truncated_normal([num_of_input, num_of_outputs], stddev=distribution))
        biases = tf.Variable(tf.constant(0.05, shape=[num_of_outputs])) # why 0.05

        layer_tensor = tf.matmul(input_tensor, weights) + biases # matmul = matrix a * matrix b => a*b and adds bias

        return layer_tensor


def max_pooling_layer(input_tensor, name, stride, ksize):

    with tf.variable_scope(name) as scope:
        layer_tensor = tf.nn.max_pool(value=input_tensor, ksize=ksize, strides=stride, padding='VALID')
        return layer_tensor


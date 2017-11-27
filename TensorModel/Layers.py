import tensorflow as flow

def conv_layer(input_, num_of_inputs, filter_size, num_of_filters, name, stride, distribution):

    with flow.variable_scope(name) as block:

        # init variables

        # filter size is nxn therfore 2 x filter size
        matrix_shape = [filter_size, filter_size, num_of_inputs, num_of_filters]

        weights = flow.Variable(flow.truncated_normal(matrix_shape, stddev=distribution))

        biases = flow.Variable(flow.constant(0.05, shape=[num_of_filters]))

        #init layer
        layer = flow.nn.conv2d(input=input_, filter=weights, strides=stride, padding='VALID')#same before

        collection = layer + biases

        return collection, weights


def fully_connected_layer(input_, num_of_input, num_of_outputs, name, distribution):

    with flow.variable_scope(name) as scope:
        weights = flow.Variable(flow.truncated_normal([num_of_input, num_of_outputs], stddev=distribution))
        biases = flow.Variable(flow.constant(0.05, shape=[num_of_outputs])) # why 0.05

        layer = flow.matmul(input_, weights) + biases # matmul = matrix a * matrix b => a*b and adds bias

        return layer


def max_pooling_layer(input_, name, stride, ksize):

    with flow.variable_scope(name) as scope:
        layer = flow.nn.max_pool(value=input_, ksize=ksize, strides=stride, padding='VALID')
        return layer


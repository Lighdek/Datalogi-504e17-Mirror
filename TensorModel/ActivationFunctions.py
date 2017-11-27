import tensorflow as flow

#todo: implement other activations
def relu_layer(input_, name):
    with flow.variable_scope(name) as scope:
        layer = flow.nn.relu(input_)
        return layer

def sigmod_layer(input_, name):
    with flow.variable_scope(name) as scope:
        layer = flow.nn.sigmoid(input_)
        return layer

def tanh_layer(input_, name):
    with flow.variable_scope(name) as scope:
        layer = flow.nn.tanh(input_)
        return layer

def relu_6_layer(input_, name):
    with flow.variable_scope(name) as scope:
        layer = flow.nn.relu6(input_)
        return layer


def leaky_relu_layer(input_, a, name):
    with flow.variable_scope(name) as scope:
        layer = flow.nn.leaky_relu(input_, a)
        return layer

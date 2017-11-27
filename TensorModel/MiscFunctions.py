import tensorflow as flow


def soft_max(input_, dim):
    with flow.variable_scope("Softmax"):
        y_pred = flow.nn.softmax(input_)
        y_pred_cls = flow.argmax(y_pred, axis=dim)
        return y_pred_cls


def cost_fucntion(input_, y_true):
    with flow.name_scope("cross_ent"):
        cross_entropy = flow.nn.softmax_cross_entropy_with_logits(logits=input_
                                                                  ,labels=y_true)
        return flow.reduce_mean(cross_entropy)

def back_propegate(cost, learning_rate):
    with flow.name_scope("optimizer"):
        return flow.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

def accuracy(y_pred_cls, y_true_cls):
    with flow.name_scope("accuracy"):
        correct_prediction = flow.equal(y_pred_cls, y_true_cls)
        return flow.reduce_mean(flow.cast(correct_prediction, flow.float32))
import tensorflow as flow
import time
import Functions as func
import Model
import collections
import numpy as np

class Config():
    num_epochs = 10
    batch_size = 10
    stride = [1, 1, 1, 1] # input shape.
    dist = 0.2

    # pool
    k_size = [1, 2, 2, 1]
    image_size = 28
    pool_stride = [1, 2, 2, 1]

    learning_rate = 1e-4 # 0.0001

def run():
    conf = Config()
    x = flow.placeholder(flow.float32, shape=[None, conf.image_size,conf.image_size, 3], name='X')# Dynamic size
    x_image = flow.reshape(x, [-1, conf.image_size, conf.image_size, 3])

    # Placeholder variable for the true labels associated with the images
    y_true = flow.placeholder(flow.float32, shape=[None, 2], name='y_true')
    y_true_cls = flow.argmax(y_true, axis=1)


    from tensorflow.examples.tutorials.mnist import input_data #TODO: new data input
    #data = input_data.read_data_sets('data/MNIST/', one_hot=True) # load data

    #make model
    model = Model.init_model(x_image, conf)

    cost = func.cost_fucntion(input_=model, y_true=y_true) # calc cost from output.
    #TODO: optimizer skal ske i reduce noden
    optimizer = func.back_propegate(cost, learning_rate=conf.learning_rate)

    y_pred_cls = func.soft_max(model, 1)  # soft max


    accuracy = func.accuracy(y_pred_cls, y_true_cls)

    # Add the cost and accuracy to summary
    flow.summary.scalar('loss', cost)
    flow.summary.scalar('accuracy', accuracy)

    # Merge all summaries together
    merged_summary = flow.summary.merge_all()

    writer = flow.summary.FileWriter("Training_FileWriter/")
    writer1 = flow.summary.FileWriter("Validation_FileWriter/")


    #data
    datam = np.random.rand(100, 28, 28, 3)
    act = np.random.randint(2, size=100*2).reshape(100, 2)
    test_batch = np.random.rand(10, 28, 28, 3)
    #test_label = np.random.randint(2, size=10).reshape(10,1)

    test_label = np.array([[0,1],
           [0,1],
           [0,1],
           [0,1],
           [1,0],
           [0,1],
           [1,0],
           [0,1],
           [1,0],
           [1,0]])

    print(test_label.shape)

    with flow.Session() as sess:
        # Initialize all variables
        sess.run(flow.global_variables_initializer())

        # Add the model graph to TensorBoard
        writer.add_graph(sess.graph)

        # Loop over number of epochs
        for epoch in range(conf.num_epochs):

            start_time = time.time()
            train_accuracy = 0

            for batch in range(0, int((act.shape[0] / conf.batch_size))):
                # Get a batch of images and labels
                x_batch = datam[batch * conf.batch_size: (batch+1) * conf.batch_size]
                y_true_batch = act[batch * conf.batch_size: (batch+1) * conf.batch_size]

                #tensor obj to np array


                feed_dict_train = {x: x_batch, y_true: y_true_batch}
                # Run the optimizer using this batch of training data.


                sess.run(optimizer, feed_dict=feed_dict_train)
                # Calculate the accuracy on the batch of training data
                train_accuracy += sess.run(accuracy, feed_dict=feed_dict_train)

                # Generate summary with the current batch of data and write to file
                summ = sess.run(merged_summary, feed_dict=feed_dict_train)
                writer.add_summary(summ, epoch * int(act.shape[0] / conf.batch_size) + batch)

            train_accuracy /= int((act.shape[0] / conf.batch_size))

            # Generate summary and validate the model on the entire validation set

            summ, vali_accuracy = sess.run([merged_summary, accuracy],
                                           feed_dict={x: test_batch, y_true: test_label})
            writer1.add_summary(summ, epoch)

            end_time = time.time()

            print("Epoch " + str(epoch + 1) + " completed : Time usage " + str(int(end_time - start_time)) + " seconds")
            print("\tAccuracy:")
            print("\t- Training Accuracy:\t{}".format(train_accuracy))
            print("\t- Validation Accuracy:\t{}".format(vali_accuracy))


run()
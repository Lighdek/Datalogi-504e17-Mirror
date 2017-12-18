from keras import backend as K

def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def fbeta_score(y_true, y_pred, beta=1):
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')

    # If there are no true positives, fix the F score at 0 like sklearn.
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return 0

    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    bb = beta ** 2
    fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
    return fbeta_score


def f1measure(y_true, y_pred):
    return fbeta_score(y_true, y_pred, beta=1)

def f_half_measure(y_true, y_pred):
    return fbeta_score(y_true, y_pred, beta=0.5)

def meanFalseNeg(y_true, y_pred):

    falseNegatives = y_true*(1-K.round(K.clip(y_pred, 0, 1)))

    numFalseNegatives = K.sum(falseNegatives)

    meanFalseNegative = K.sum(y_pred * falseNegatives) / numFalseNegatives

    return meanFalseNegative

def meanFalsePos(y_true, y_pred):
    falsePositives = (1 - y_true) * (K.round(K.clip(y_pred, 0, 1)))

    numFalsePositives = K.sum(falsePositives)

    meanFalsePositives = K.sum(y_pred * falsePositives) / numFalsePositives

    return meanFalsePositives

def minFalseNeg(y_true, y_pred):

    falseNegatives = y_true*(1-K.round(K.clip(y_pred, 0, 1)))

    minFalseNegative = 1 - K.max((1 - K.round(K.clip(y_pred, 0, 1))) * falseNegatives)

    return minFalseNegative

def maxFalsePos(y_true, y_pred):
    falsePositives = (1 - y_true) * (K.round(K.clip(y_pred, 0, 1)))

    maxFalsePositives = K.max((K.round(K.clip(y_pred, 0, 1))) * falsePositives)

    return maxFalsePositives

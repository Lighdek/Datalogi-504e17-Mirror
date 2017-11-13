from pyspark.ml.pipeline import Pipeline, PipelineModel
from pyspark.ml.classification import MultilayerPerceptronClassifier

from pyspark.ml.linalg import Vectors

from pyspark.shell import spark

model = Pipeline(stages=[
MultilayerPerceptronClassifier()
])


df = spark.createDataFrame([
    (0.0, Vectors.dense([0.0, 0.0])),
    (1.0, Vectors.dense([0.0, 1.0])),
    (1.0, Vectors.dense([1.0, 0.0])),
    (0.0, Vectors.dense([1.0, 1.0]))], ["label", "features"])
mlp = MultilayerPerceptronClassifier(maxIter=100, layers=[2, 2, 2], blockSize=1, seed=123)
model = mlp.fit(df)
print(model.layers)
print(model.weights.size)
testDF = spark.createDataFrame([
    (Vectors.dense([1.0, 0.0]),),
    (Vectors.dense([0.0, 0.0]),)], ["features"])
print(model.transform(testDF).show())


# mlp2 = MultilayerPerceptronClassifier.load(mlp_path)
# print(mlp2.getBlockSize())



#     >>> model_path = temp_path + "/mlp_model"
#     >>> model.save(model_path)
#     >>> model2 = MultilayerPerceptronClassificationModel.load(model_path)
#     >>> model.layers == model2.layers
#     True
#     >>> model.weights == model2.weights
#     True
#     >>> mlp2 = mlp2.setInitialWeights(list(range(0, 12)))
#     >>> model3 = mlp2.fit(df)
#     >>> model3.weights != model2.weights
#     True
#     >>> model3.layers == model.layers
#     True
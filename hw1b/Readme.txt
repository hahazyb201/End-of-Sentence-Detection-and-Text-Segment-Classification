Convert data to ARFF format file:
python convertToArff.py data_file

Weka classifier:
weka.classifiers.trees.RandomForest -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1

Result:
Correctly Classified Instances(cross-validation)  99.4399 %
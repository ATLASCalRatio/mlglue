#import xgboost
import numpy as np
from mlglue.tree import tree_to_tmva, BDTxgboost, BDTsklearn
from sklearn.datasets import load_svmlight_files
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

import unittest

def setUp_all(self):
    self.data_x, self.data_y = data[0].todense(), data[1]
    self.data_y_binary = (self.data_y>5).astype(np.int32)
    self.features = ["f{0}".format(i) for i in range(self.data_x.shape[1])]

class TestBDTxgboost(unittest.TestCase):

    def setUp(self):
        setUp_all(self)

    #do a binary classification
    def test_classify_binary(self):
        print ("TestBDTxgboost test_classify_binary")
        model = xgboost.XGBClassifier(n_estimators=10)
        model.fit(self.data_x, self.data_y_binary)

        bdt = BDTxgboost(model, self.features, ["cls0", "cls1"])

        bdt.to_tmva("xgb_binary.xml")
        bdt.setup_tmva("xgb_binary.xml")

        dev = 0.0
        for irow in range(self.data_x.shape[0]):
            predA = bdt.eval_tmva(self.data_x[irow, :])
            predB = bdt.eval(self.data_x[irow, :])
            local_dev = np.abs((predA - predB)/predA)
            self.assertTrue(local_dev < 0.05)

            dev += local_dev
        self.assertTrue(dev < 0.01)

class TestBDTsklearn(unittest.TestCase):

    def setUp(self):
        setUp_all(self)

    #do a binary classification
    def test_classify_binary(self):
        print ("TestBDTsklearn test_classify_binary")
        model = GradientBoostingClassifier(n_estimators=10)
        model.fit(self.data_x, self.data_y_binary)

        bdt = BDTsklearn(model, self.features, ["cls0", "cls1"])

        bdt.to_tmva("sklearn_binary.xml")
        bdt.setup_tmva("sklearn_binary.xml")

        dev = 0.0
        for irow in range(self.data_x.shape[0]):
            predA = bdt.eval_tmva(self.data_x[irow, :])
            predB = bdt.eval(self.data_x[irow, :])
            local_dev = np.abs((predA - predB)/predA)
            self.assertTrue(local_dev < 0.05)

            dev += local_dev
        self.assertTrue(dev < 0.01)

    #do a binary classification
    def test_classify_multiclass(self):
        print ("TestBDTsklearn test_classify_multiclass")
        model = GradientBoostingClassifier(n_estimators=10)
        model.fit(self.data_x, self.data_y)

        bdt = BDTsklearn(model, self.features, ["cls{0}".format(c) for c in range(len(np.unique(self.data_y)))])

        bdt.to_tmva("sklearn_multiclass.xml")
        bdt.setup_tmva("sklearn_multiclass.xml")

        dev = 0.0
        for irow in range(self.data_x.shape[0]):
            predA = bdt.eval_tmva(self.data_x[irow, :])
            predB = bdt.eval(self.data_x[irow, :])
            local_dev = np.abs((predA - predB)/predA)
            self.assertTrue(np.all(local_dev < 0.05))

            dev += local_dev
        self.assertTrue(np.all(dev < 0.01))

    #do a binary classification
    def test_classify_ada_multiclass(self):
        print ("TestBDTsklearn test_classify_ada_multiclass")
        model = AdaBoostClassifier(
            DecisionTreeClassifier(max_depth=3),
            n_estimators=5,
            learning_rate=1)
        model.fit(self.data_x, self.data_y)

        bdt = BDTsklearn(model, self.features, ["cls{0}".format(c) for c in range(len(np.unique(self.data_y)))])

        bdt.to_tmva("sklearn_ada_multiclass.xml")
        bdt.setup_tmva("sklearn_ada_multiclass.xml")

        dev = 0.0
        for irow in range(self.data_x.shape[0]):
            predA = bdt.eval_tmva(self.data_x[irow, :])
            predB = bdt.eval(self.data_x[irow, :])
            local_dev = np.abs((predA - predB)/predA)

            if np.any(local_dev >= 0.05):
                print ("TMVA: {0}".format(predA))
                print ("Generalized Tree: {0}".format(predB))
                print ("Difference: {0}".format(local_dev))

            self.assertTrue(np.all(local_dev < 0.05))

            dev += local_dev
        self.assertTrue(np.all(dev < 0.01))

    #do a binary classification
    def test_regression(self):
        print ("TestBDTsklearn test_classify_multiclass")
        model = GradientBoostingRegressor(n_estimators=10)
        model.fit(self.data_x, self.data_y)

        bdt = BDTsklearn(model, self.features, ["target"])

        bdt.to_tmva("sklearn_regression.xml")
        bdt.setup_tmva("sklearn_regression.xml")

        dev = 0.0
        for irow in range(self.data_x.shape[0]):
            predA = bdt.eval_tmva(self.data_x[irow, :])
            predB = bdt.eval(self.data_x[irow, :])
            local_dev = np.abs((predA - predB)/predA)
            self.assertTrue(np.all(local_dev < 0.05))

            dev += local_dev
        self.assertTrue(np.all(dev < 0.01))

#use this to debug
def simple_test_xgboost():
    data_x, data_y = data[0][:1000, :5], data[1][:1000]
    data_y_binary = (data_y>5).astype(np.int32)

    print ("Binary classification")
    print ("training model")
    model = xgboost.XGBClassifier(n_estimators=10)
    model.fit(data_x, data_y_binary)

    features = ["f{0}".format(i) for i in range(data_x.shape[1])]
    target_names = ["cls{0}".format(i) for i in range(len(np.unique(data_y_binary)))]

    bdt = BDTxgboost(model, features, target_names)
    bdt.to_tmva("test.xml")
    bdt.setup_tmva("test.xml")

    d1 = 0.0
    for irow in range(data_x.shape[0]):
        predA1 = bdt.eval_tmva(data_x[irow, :])
        predB1 = bdt.eval(data_x[irow, :])
        d1 += np.abs((predA1 - predB1)/predA1)

if __name__ == "__main__":
    print ("fetching data")
    data = load_svmlight_files(("usps", "usps.t"))

    #simple_test_xgboost()
    unittest.main()

# mlglue

This python 3 library contains tools to simplify conversion between models in different machine learning libraries.
In particular, it contains conversion code Gradient Boosted Decision Trees for `sklearn -> TMVA` and `xgboost -> TMVA`.
Binary classification, multiclass and regression trees are supported.

Exporting to TMVA XML:
~~~
╔════════════╦═════════╦═════════╗
║    type    ║ sklearn ║ xgboost ║
╠════════════╬═════════╬═════════╣
║ binary     ║ x       ║ x       ║
║ multiclass ║ x       ║         ║
║ regression ║ x       ║         ║
╚════════════╩═════════╩═════════╝
~~~

### Installation

Clone this repository, install with
~~~
python setup.py install
~~~

You'll need to make sure that scipy, numpy, and sklearn are all installed (using pip3) for this package to work.

To run the tests you'll need to download the following two data files and place them in the directory where you run the tests:

- http://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/usps.bz2 
- http://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/usps.t.bz2 

### Quickstart

Here is a small example
~~~
model = xgboost.XGBClassifier(n_estimators=10)
model.fit(data_x, data_y_binary)

num_features = data_x.shape[1]
features = ["feat{0}".format(nf) for nf in range(num_features)]
target_names = ["cls0", "cls1"]

bdt = BDTxgboost(model, features, target_names)
bdt.to_tmva("test.xml")
bdt.setup_tmva("test.xml")
for irow in range(data_x.shape[0]):
    predA = bdt.eval_tmva(data_x[irow, :])
    predB = bdt.eval(data_x[irow, :])
~~~

Check out `test/test_all.py` for an overview and the testsuite.

# LICENSE

This program is licensed under the GPLv3 license, see LICENSE.md for details.


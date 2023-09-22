import sys

import numpy as np
import scipy.stats as st
from scipy.stats import pearsonr, hmean, gmean, spearmanr, rankdata
import sklearn.metrics as sk
import tools.convert_tests as conv


def get_predicted_scores(lines, f = lambda x: x.split()[-1]):
    out = []
    for i,l in enumerate(lines):
        try:
            x = f(l)
            x = float(x)
            out.append(x)
        except:
            out.append("NA")
    return np.array(out[0:len(lines)])


def readl(p):
    with open(p) as f:
        return f.read().split("\n")


def evaluate_with_function(ys, xs, fun):
    return fun(ys, xs)

def area_uc(ys, xs):
    assert len(xs) == len(ys)
    fpr, tpr, thresholds = sk.roc_curve(ys, xs, pos_label=1)
    aucval = sk.auc(fpr, tpr)
    return aucval


def perc(xs, t=5):
    xsi = enumerate(xs)
    print(xs, len(xs))
    xsi = sorted(xsi, key=lambda x:x[1], reverse=True)
    p = int((len(xsi)/100)*t)
    print(p)
    pxsi = xsi[:p]
    nxsi = xsi[p:]
    new = [0.0] * len(xs)

    for i, _ in pxsi:
        new[i] = 1
    for i, _ in nxsi:
        new[i] = 0

    print(new)
    sys.exit(-1)

    return new

def acc_of_ones(ys, xs, t=5):
    ys = [int(x) for x in ys]
    xs = perc(xs, t)
    s = 0.0
    for i, x in enumerate(xs):
        if x == 1:
            s += ys[i]
    s /= max(1, sum(xs))
    return s

def acc_of_ones_thres(ys, xs, thres=[1, 2, 3, 4, 5, 7, 10, 15]):
    out = []
    for t in thres:
        out.append(acc_of_ones(ys, xs, t))
    return out

def remove_undecided(gold, pred, returnkeepids=False):
    
    ids = [i for i in range(len(gold)) if gold[i] == "undecided"]
    kids = [i for i in range(len(gold)) if gold[i] != "undecided"]
    gold = [gold[i] for i in range(len(gold)) if i not in ids]
    pred = [pred[i] for i in range(len(pred)) if i not in ids]

    if returnkeepids:
        return gold, pred, kids
    
    return gold, pred





def convert_labels(labels):
    labels = labels.strip().split("\n")
    conv_labels = []
    for it in labels:
        if it == "None":
            it = 1
        elif it == "True":
            it = 0
        elif it == "False":
            it = 2
        else:
            it = "undecided"
        conv_labels.append(it)
    return conv_labels


if __name__ == "__main__":

    benchmarks = ["sick", "fracas", "hans", "allen"]

    if len(sys.argv) >1:
        if sys.argv[1] in benchmarks:
            benchmarks = [sys.argv[1]]

    evalfun = area_uc
    if len(sys.argv) > 2:
        evalfun = acc_of_ones_thres

    scores = []

    # default evaluation function

    # use this function for evaluating according to thresholds


    for bench in benchmarks:
        pred = conv.read_prediction(bench)
        gold = conv.read_gold_labels(bench)

        gold = convert_labels(gold)

        gold, pred = remove_undecided(gold, pred)

        score = evaluate_with_function(gold, pred, fun=evalfun)
        scores.append(score)
        print(f"Score ({bench}): {score}")

    print(scores)

    scores_without_sick = scores[1:]
    print(scores_without_sick)
    
    if isinstance(scores[0], list):
        scores = np.array(scores)
        scores_without_sick = np.mean(scores[1:], axis=0).T
        scores = np.mean(scores, axis=0).T
     
    scores = [round(sc * 100, 1) for sc in scores] + [round(np.mean(scores) * 100, 1)] + [round(np.mean(scores_without_sick) * 100, 1)]
    scores = [str(sc) for sc in scores]
    print("\nmean score", scores[-2])
    print("mean score without SICK", scores[-1])

    scores = " & ".join(scores)
    scores = scores + " \\\\"
    print(scores, "\n")

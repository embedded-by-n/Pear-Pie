# train the scikit-learn model on the logged data.
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

import analysis
import config
import pod_registry

def prepare_features(df):
    """Features X, target y. Given (hour, day-of-week, current space) predict
    the NEXT space. 'from' is encoded with pod_registry.space_code so the same
    mapping is reproducible at prediction time (this was the bug: pandas
    category codes were not reproducible)."""
    moves = analysis.movements(df)
    if moves.empty or len(moves) < 5:
        return None, None

    moves = moves.copy()
    moves["dt"] = pd.to_datetime(moves["at"], unit="s")
    moves["hour"] = moves["dt"].dt.hour
    moves["dow"] = moves["dt"].dt.dayofweek
    moves["from_code"] = moves["from"].map(pod_registry.space_code)

    X = moves[["hour", "dow", "from_code"]]
    y = moves["to"]
    return X, y

def train(X, y):
    model = DecisionTreeClassifier(max_depth=6, min_samples_leaf=2)
    model.fit(X, y)
    return model

def evaluate(model, X, y):
    if len(X) < 10:
        return accuracy_score(y, model.predict(X))
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, random_state=0)
    model.fit(X_tr, y_tr)
    return accuracy_score(y_te, model.predict(X_te))

def save(model, path=None):
    path = path or config.MODEL_FILE
    joblib.dump(model, path)
    return path

def run(path=None):
    df = analysis.load_log(path)
    X, y = prepare_features(df)
    if X is None:
        print("not enough movement data to train yet")
        return None
    model = train(X, y)
    score = evaluate(model, X, y)
    print("trained. holdout accuracy: %.2f" % score)
    save(model)
    print("saved model ->", config.MODEL_FILE)
    return model

if __name__ == "__main__":
    run()

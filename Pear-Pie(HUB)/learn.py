# train the scikit-learn model on the logged data.
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

import analysis
import config

def prepare_features(df):
    """Turn the log/analysis into features X and targets y for training.

    Task framed as: given (hour, day-of-week, current space), predict the
    NEXT space the user moves to. That learned pattern is what the hub uses
    to decide whether a pod's sensitivity still fits the user's rhythm.
    """
    moves = analysis.movements(df)
    if moves.empty or len(moves) < 5:
        return None, None

    moves = moves.copy()
    moves["dt"] = pd.to_datetime(moves["at"], unit="s")
    moves["hour"] = moves["dt"].dt.hour
    moves["dow"] = moves["dt"].dt.dayofweek

    # encode the 'from' space as a category code
    moves["from_code"] = moves["from"].astype("category").cat.codes

    X = moves[["hour", "dow", "from_code"]]
    y = moves["to"]
    return X, y

def train(X, y):
    """Train the model. (the course's fit/score pipeline.)"""
    model = DecisionTreeClassifier(max_depth=6, min_samples_leaf=2)
    model.fit(X, y)
    return model

def evaluate(model, X, y):
    """Score it. (the course's evaluation step.)"""
    if len(X) < 10:
        # too little data to hold out; score on what we have
        return accuracy_score(y, model.predict(X))
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, random_state=0)
    model.fit(X_tr, y_tr)
    return accuracy_score(y_te, model.predict(X_te))

def save(model, path=None):
    """Persist the trained model."""
    path = path or config.MODEL_FILE
    joblib.dump(model, path)
    return path

def run(path=None):
    """Full pipeline: load -> features -> train -> evaluate -> save."""
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

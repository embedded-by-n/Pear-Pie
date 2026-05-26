#train the scikit-learn model on the logged data.
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import analysis

def prepare_features(df):
    """Turn the log/analysis into features X and targets y for training."""
    # TODO

def train(X, y):
    """Train the model. (the course's fit/score pipeline.)"""
    model = DecisionTreeClassifier()
    # TODO: model.fit(X, y)
    return model

def evaluate(model, X, y):
    """Score it. (the course's evaluation step.)"""
    # TODO

def save(model, path):
    """Persist the trained model."""
    # TODO
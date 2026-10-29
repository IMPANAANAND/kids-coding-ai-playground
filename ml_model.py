"""Standard-library-only fruit features and k-nearest-neighbours classifier."""
import random

K_NEIGHBOURS = 3


def knn_predict(training_data, features, k=K_NEIGHBOURS):
    """Classify using majority label among the k closest examples.

    Features are normalized color (0..1) and size (0..1). Each example is
    ``(feature_vector, label)``. A vote tie goes to the closest tied example.
    """
    if k < 1:
        raise ValueError("k must be at least 1.")
    if len(training_data) < k:
        raise ValueError(f"Please provide at least {k} labelled examples.")
    distances = []
    for vector, label in training_data:
        if len(vector) != len(features):
            raise ValueError("Training examples and prediction must use the same features.")
        distance = sum((a-b)**2 for a,b in zip(vector,features)) ** 0.5
        distances.append((distance,label))
    nearest = sorted(distances, key=lambda item:item[0])[:k]
    votes = {}
    for distance,label in nearest:
        votes[label] = votes.get(label,0)+1
    top = max(votes.values())
    tied = [label for label,count in votes.items() if count == top]
    if len(tied)==1: return tied[0]
    return next(label for _,label in nearest if label in tied)


def make_fruit(kind=None):
    """Create a fruit and its normalized color and size feature vector."""
    kind = kind or random.choice(["apple","orange"])
    base = .12 if kind == "apple" else .87
    return {"kind":kind,"features":[max(0,min(1,random.gauss(base,.13))),random.uniform(.30,.90)]}

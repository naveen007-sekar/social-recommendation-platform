import numpy as np
from app.utils.helpers import cosine, vector
from app.recommender.ranker import score
def test_cosine_and_bad_vectors():
    assert cosine(np.array([1.,0.]),np.array([1.,0.])) == 1.
    assert cosine(np.array([1.]),np.array([1.,0.])) == 0.
    assert vector(["bad"]) is None
def test_weighted_score_is_bounded():
    assert 0 <= score({"content":1,"popularity":1}) <= 1

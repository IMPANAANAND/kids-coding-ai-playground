"""Small standard-library checks for the actual k-NN prediction function."""
import unittest
from ml_model import knn_predict


class KnnTests(unittest.TestCase):
    def setUp(self):
        self.examples = [([.08,.45],"apple"),([.15,.60],"apple"),
                         ([.88,.50],"orange"),([.80,.70],"orange")]

    def test_nearby_examples_decide_prediction(self):
        self.assertEqual(knn_predict(self.examples,[.12,.52]),"apple")
        self.assertEqual(knn_predict(self.examples,[.85,.55]),"orange")

    def test_labels_are_learned_from_training_data(self):
        reversed_examples = [(features,"orange" if label=="apple" else "apple") for features,label in self.examples]
        self.assertEqual(knn_predict(reversed_examples,[.12,.52]),"orange")

    def test_requires_at_least_k_examples(self):
        with self.assertRaises(ValueError): knn_predict(self.examples[:2],[.1,.5])


if __name__=="__main__": unittest.main()

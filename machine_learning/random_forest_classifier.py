# Random Forest Classifier Example

from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split


def random_forest_accuracy() -> float:
    """
    Train a random forest on the Iris dataset and return its test accuracy.

    >>> random_forest_accuracy() > 0.9
    True
    """
    iris = load_iris()
    features_train, features_test, targets_train, targets_test = train_test_split(
        iris["data"], iris["target"], test_size=0.3, random_state=42
    )
    classifier = RandomForestClassifier(random_state=42, n_estimators=100)
    classifier.fit(features_train, targets_train)
    return classifier.score(features_test, targets_test)


def main() -> None:
    """
    Random Forest Classifier Example using sklearn function.
    Iris type dataset is used to demonstrate algorithm.
    """
    # Load Iris dataset
    iris = load_iris()

    # Split dataset into train and test data
    x = iris["data"]  # features
    y = iris["target"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=1
    )

    # Random Forest Classifier
    rand_for = RandomForestClassifier(random_state=42, n_estimators=100)
    rand_for.fit(x_train, y_train)

    # Display Confusion Matrix of Classifier
    ConfusionMatrixDisplay.from_estimator(
        rand_for,
        x_test,
        y_test,
        display_labels=iris["target_names"],
        cmap="Blues",
        normalize="true",
    )
    plt.title("Normalized Confusion Matrix - IRIS Dataset")
    plt.show()


if __name__ == "__main__":
    main()

# This file contains the code of the Random Forest classifier
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score


# This function is used to train and evaluate the classifier
def train_and_evaluate_classifier(X_train, y_train, X_test, y_test):
    """
    Trains a classifier using the training set and evaluates its performance using the test set.

    :param X_train: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the training set of the dataset)
    :param y_train: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the training set of the dataset)
    :param X_test: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the test set of the dataset)
    :param y_test: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the test set of the dataset)

    :return: A tuple containing the model's accuracy and the classification report.
    """

    # Uncomment the following lines of code to see the accuracy of the model with different number of trees
    """ 
    print("\nAccuracy with different number of trees:\n")

    for n_trees in [50, 100, 200, 300, 400, 500]:
        model = RandomForestClassifier(n_estimators=n_trees, random_state=14)

        # Combine X_train and X_test, and y_train and y_test
        X_combined = np.concatenate((X_train, X_test), axis=0)
        y_combined = np.concatenate((y_train, y_test), axis=0)

        scores = cross_val_score(model, X_combined, y_combined, cv=3)
        print(f'n_estimators={n_trees}, Scores mean: {scores.mean()}')
    """

    # Uncomment the following lines of code to scale features
    """
    # Scale the features
    scaler = MinMaxScaler()

    scaled_X_train = scaler.fit_transform(X_train)
    scaled_X_test = scaler.fit_transform(X_test)
    """

    model = RandomForestClassifier(n_estimators=400, random_state=42, min_samples_leaf=1, min_samples_split=2, max_depth=None)

    # Train the final model with the training data
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model performance and print the results
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    # Return the accuracy and classification report
    return accuracy, report

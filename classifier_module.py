# This file contains the code of the Random Forest and XGBoost classifiers

import joblib
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# TODO: provide support for the hyperparameters tuning of the classifiers (Random Forest and XGBoost)

# This function is used to train and evaluate the Random Forest classifier
def train_and_test_rf_classifier(X_train, y_train, X_test, y_test):
    """
    Trains a classifier using the training set and evaluates its performance using the test set.

    :param X_train: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the training set of the dataset)
    :param y_train: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the training set of the dataset)
    :param X_test: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the test set of the dataset)
    :param y_test: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the test set of the dataset)

    :return: A tuple containing the model's accuracy and the classification report.
    """

    model = RandomForestClassifier(n_estimators=400, random_state=42, min_samples_leaf=1, min_samples_split=2, max_depth=None)

    # Train the final model with the training data
    model.fit(X_train, y_train)

    # Save the trained model to a file
    save_model(model, 'trained_rf_classifier.pkl')

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model performance and print the results
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    # Return the accuracy and classification report
    return accuracy, report



# This function is used to train and evaluate the XGBoost classifier
def train_and_test_xgb_classifier(X_train, y_train, X_test, y_test):
    """
    Trains a classifier using the training set and evaluates its performance using the test set.

    :param X_train: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the training set of the dataset)
    :param y_train: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the training set of the dataset)
    :param X_test: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the test set of the dataset)
    :param y_test: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the test set of the dataset)

    :return: A tuple containing the model's accuracy and the classification report.
    """

    model = XGBClassifier()

    # Train the final model with the training data
    model.fit(X_train, y_train)

    # Save the trained model to a file
    save_model(model, 'trained_xgb_classifier.pkl')

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model performance and print the results
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    # Return the accuracy and classification report
    return accuracy, report

# This function is used to save the trained model to a file
def save_model(model, file_name):
    """
    Saves the trained model to a file.

    :param model: The trained model to be saved.
    :param file_name: The name of the file where the model will be saved.
    """
    joblib.dump(model, file_name)
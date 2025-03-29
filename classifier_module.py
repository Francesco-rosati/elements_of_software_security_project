# This file contains the code of the Random Forest and XGBoost classifiers

import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV


# This function is used to train and evaluate the Random Forest classifier
def train_and_test_rf_classifier(X_train, y_train, X_test, y_test, delta):
    """
    Trains a classifier using the training set and evaluates its performance using the test set.

    :param X_train: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the training set of the dataset)
    :param y_train: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the training set of the dataset)
    :param X_test: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the test set of the dataset)
    :param y_test: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the test set of the dataset)
    :param delta: The delta value used for the analysis.

    :return: A tuple containing the model's accuracy and the classification report.
    """

    # Initialize the Random Forest classifier and find the best hyperparameters
    model = tune_rf_hyperparameters(X_train, y_train)

    # Train the final model with the training data
    model.fit(X_train, y_train)

    # Save the trained model to a file
    save_model(model, 'rf_models', f'trained_rf_classifier_{delta}.pkl')

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model performance and print the results
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    # Return the accuracy and classification report
    return accuracy, report


# This function is used to tune the hyperparameters of the Random Forest classifier
def tune_rf_hyperparameters(X_train, y_train):
    """
    Performs hyperparameter tuning for Random Forest using GridSearchCV.

    :param X_train: Feature matrix for training.
    :param y_train: Labels for training data.
    :return: Best trained model with optimized hyperparameters.
    """
    param_grid = {
        'n_estimators': [100, 200, 400],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'random_state': [42]
    }

    model = RandomForestClassifier()
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print("Best parameters for Random Forest:", grid_search.best_params_)
    return grid_search.best_estimator_


# This function is used to train and evaluate the XGBoost classifier
def train_and_test_xgb_classifier(X_train, y_train, X_test, y_test, delta):
    """
    Trains a classifier using the training set and evaluates its performance using the test set.

    :param X_train: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the training set of the dataset)
    :param y_train: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the training set of the dataset)
    :param X_test: Array-like or matrix of shape (n_samples, n_features) representing the features. (from the test set of the dataset)
    :param y_test: Array-like of shape (n_samples) representing the class labels associated with the features in X. (from the test set of the dataset)
    :param delta: The delta value used for the analysis.

    :return: A tuple containing the model's accuracy and the classification report.
    """

    # Initialize the XGBoost classifier and find the best hyperparameters
    model = tune_xgb_hyperparameters(X_train, y_train)

    # Train the final model with the training data
    model.fit(X_train, y_train)

    # Save the trained model to a file
    save_model(model, 'xgb_models', f'trained_xgb_classifier_{delta}.pkl')

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model performance and print the results
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    # Return the accuracy and classification report
    return accuracy, report


# This function is used to tune the hyperparameters of the XGBoost classifier
def tune_xgb_hyperparameters(X_train, y_train):
    """
    Performs hyperparameter tuning for XGBoost using GridSearchCV.

    :param X_train: Feature matrix for training.
    :param y_train: Labels for training data.
    :return: Best trained model with optimized hyperparameters.
    """
    param_grid = {
        'n_estimators': [100, 200, 400],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 6, 10],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
        'random_state': [42]
    }

    model = XGBClassifier()
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print("Best parameters for XGBoost:", grid_search.best_params_)
    return grid_search.best_estimator_


# This function is used to save the trained model to a file
def save_model(model, directory_name, file_name):
    """
    Saves the trained model to a file.

    :param model: The trained model to be saved.
    :param directory_name: The name of the directory where the model will be saved.
    :param file_name: The name of the file where the model will be saved.
    """

    # Create the directory if it does not exist
    os.makedirs(directory_name, exist_ok=True)

    # Full path for saving the model
    file_path = os.path.join(directory_name, file_name)

    joblib.dump(model, file_path)
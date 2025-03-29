import os
import sys
from colorama import Fore, Style
from sklearn.model_selection import train_test_split
from classifier_module import train_and_evaluate_rf_classifier, train_and_evaluate_xgb_classifier
from dataset_formatter import read_training_files

# defining the delta value
delta = 20

# Get dataset folder path from command line
if len(sys.argv) < 2:
    print(f'\n{Fore.RED}ERROR: You must provide a dataset folder path as command line arguments!{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}Usage: python {sys.argv[0]} <dataset folder path> <dataset type>{Style.RESET_ALL}')
    sys.exit(1)

# Dataset folder path and name
main_folder_path = str(sys.argv[1])
main_folder_name = main_folder_path.split('/')[-1]

# Training and evaluation set folder paths
training_folder_path = f'{main_folder_path}/training - test set'
evaluation_folder_path = f'{main_folder_path}/evaluation set'

# Output folder paths
output_training_folder_path = f'{training_folder_path}/classification_results/'
output_evaluation_folder_path = f'{evaluation_folder_path}/classification_results/'

# Start the analysis of the training dataset

print(f'\n{Fore.YELLOW}Starting analysis for folder: {Style.RESET_ALL}{main_folder_name}{Fore.YELLOW} with{Style.RESET_ALL} delta = {delta}')

# Read data from dataset (The same dataset is used to train and test the model)
X, y = read_training_files(training_folder_path, f'{main_folder_name}/training - test set', delta)

# Split the dataset into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=None)

# Train and evaluate the classifiers

print(f'\n{Fore.MAGENTA}Training and testing the Random Forest classifier...{Style.RESET_ALL}')

# Train and evaluate the Random Forest classifier
accuracyRF, reportRF = train_and_evaluate_rf_classifier(X_train, y_train, X_test, y_test)

print(f'\n{Fore.GREEN}Model successfully trained and tested...{Style.RESET_ALL}')

print(f'\n{Fore.MAGENTA}Training and evaluating the XGBoost classifier...{Style.RESET_ALL}')

# Train and evaluate the XGBoost classifier
accuracyXGB, reportXGB = train_and_evaluate_xgb_classifier(X_train, y_train, X_test, y_test)

print(f'\n{Fore.GREEN}Model successfully trained and tested...{Style.RESET_ALL}')

# Create the output folder if it doesn't exist
os.makedirs(output_training_folder_path, exist_ok=True)

# Write results to the output file
with open(f'{output_training_folder_path}/training_{main_folder_name}_{delta}_results.txt', 'w') as file:

    print(f'\n{Fore.YELLOW}Writing results for folder: {Style.RESET_ALL}{main_folder_name}/training - test set')

    # Write results to file
    file.write(f'Results for folder {main_folder_name} are:\n')
    file.write(f'\nRandom Forest Accuracy: {accuracyRF:.3f}\n')
    file.write(f'\nRandom Forest Classification Report: \n\n{reportRF}\n\n')

    file.write(f'\nXGBoost Accuracy: {accuracyXGB:.3f}\n')
    file.write(f'\nXGBoost Classification Report: \n\n{reportXGB}')

    print(f'\n{Fore.GREEN}Results successfully written!{Style.RESET_ALL}')
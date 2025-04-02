import os
import sys
from colorama import Fore, Style
from sklearn.model_selection import train_test_split
from evaluation_modules.evaluation_module import evaluate_realistic_scenario
from training_test_modules.classifier_module import train_and_test_rf_classifier, train_and_test_xgb_classifier
from training_test_modules.dataset_formatter import read_training_files

# Defining the delta value
delta = 20

# Get dataset folder path from command line
if len(sys.argv) < 3:
    print(f'\n{Fore.RED}ERROR: You must provide a dataset folder path and evaluation state as command line arguments!{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}Usage: python {sys.argv[0]} <dataset folder path> <evaluation state ("yes" or "no")>{Style.RESET_ALL}')
    sys.exit(1)

# Dataset folder path and name
main_folder_path = str(sys.argv[1])
main_folder_name = main_folder_path.split('/')[-1]

# Evaluation bool
evaluation_state = str(sys.argv[2]).lower()

# Training and evaluation set folder paths
training_folder_path = f'{main_folder_path}/training - test set'
evaluation_folder_path = None
output_evaluation_folder_path = None

if evaluation_state == "yes":
    evaluation_folder_path = f'{main_folder_path}/evaluation set'

# Output folder paths
output_training_folder_path = f'{training_folder_path}/classification_results/'

if evaluation_state == "yes":
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
accuracyRF, reportRF = train_and_test_rf_classifier(X_train, y_train, X_test, y_test, delta)

print(f'\n{Fore.GREEN}Model successfully trained and tested...{Style.RESET_ALL}')

print(f'\n{Fore.MAGENTA}Training and evaluating the XGBoost classifier...{Style.RESET_ALL}')

# Train and evaluate the XGBoost classifier
accuracyXGB, reportXGB = train_and_test_xgb_classifier(X_train, y_train, X_test, y_test, delta)

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


# TODO: Complete code for evaluation set
if evaluation_state == "yes" and evaluation_folder_path is not None and output_evaluation_folder_path is not None:

    print(f'\n{Fore.YELLOW}Starting evaluation for folder: {Style.RESET_ALL}{main_folder_name}{Fore.YELLOW} with{Style.RESET_ALL} delta = {delta}')

    # Evaluate the realistic scenario
    evaluate_realistic_scenario(evaluation_folder_path, delta)

    print(f'\n{Fore.GREEN}Evaluation successfully completed!{Style.RESET_ALL}')
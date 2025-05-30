import os
import sys
from colorama import Fore, Style
from sklearn.model_selection import train_test_split
from evaluation_modules.evaluation_module import evaluate_user_scenarios
from evaluation_modules.evaluation_utilities import write_window_results
from training_test_modules.classifier_module import train_and_test_rf_classifier, train_and_test_xgb_classifier
from training_test_modules.dataset_formatter import read_training_files

# Define the delta value
# The delta value is the time window used to split the packets into smaller windows for analysis.
delta = 5

# Get dataset folder path from command line
if len(sys.argv) < 2:
    print(f'\n{Fore.RED}ERROR: You must provide the dataset folder path as a command line argument!{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}Usage: python {sys.argv[0]} <dataset folder path>{Style.RESET_ALL}')
    sys.exit(1)

# Dataset folder path and name
main_folder_path = str(sys.argv[1])
main_folder_name = main_folder_path.split('/')[-1]

# Define folder paths for training and output
training_folder_path = os.path.join(main_folder_path, 'training - test set')
output_training_folder_path = os.path.join(training_folder_path, 'classification_results')

# Define model file paths in their respective folders
rf_model_path = os.path.join('rf_models', f'trained_rf_classifier_{delta}.pkl')
xgb_model_path = os.path.join('xgb_models', f'trained_xgb_classifier_{delta}.pkl')

# General function to ask the user a yes/no question
def ask_user(question):
    response = ""
    while response not in {"yes", "no"}:
        response = input(f'\n{Fore.CYAN}{question} (yes/no): {Style.RESET_ALL}').strip().lower()
        if response not in {"yes", "no"}:
            print(f'{Fore.RED}Invalid input! Please enter "yes" or "no".{Style.RESET_ALL}')
    return response == "yes"

# Function to ask for evaluation confirmation
def ask_for_evaluation():
    return ask_user("Do you want to proceed with model evaluation?")

# Function to ask if the user wants to retrain the models
def ask_for_retraining():
    return ask_user("Pre-trained models found! Do you want to retrain the models?")

# Function to perform training and writing of results
def run_training():
    # Start the analysis of the training dataset
    print(
        f'\n{Fore.CYAN}No models found!{Style.RESET_ALL}\n\n{Fore.YELLOW}Starting analysis for folder: {Style.RESET_ALL}{main_folder_name}{Fore.YELLOW} with{Style.RESET_ALL} delta = {delta}')

    # Read data from dataset (The same dataset is used to train and test the model)
    X, y = read_training_files(training_folder_path, f'{main_folder_name}/training - test set', delta)

    # Split the dataset into training and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=None)

    # Train and evaluate the Random Forest classifier
    print(f'\n{Fore.MAGENTA}Training and testing the Random Forest classifier...{Style.RESET_ALL}')
    accuracyRF, reportRF = train_and_test_rf_classifier(X_train, y_train, X_test, y_test, delta)
    print(f'\n{Fore.GREEN}Model successfully trained and tested!{Style.RESET_ALL}')

    # Train and evaluate the XGBoost classifier
    print(f'\n{Fore.MAGENTA}Training and evaluating the XGBoost classifier...{Style.RESET_ALL}')
    accuracyXGB, reportXGB = train_and_test_xgb_classifier(X_train, y_train, X_test, y_test, delta)
    print(f'\n{Fore.GREEN}Model successfully trained and tested!{Style.RESET_ALL}')

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


# Variables to decide if training and evaluation should be performed
perform_training = False
perform_evaluation = False

# Check if the model files already exist
if os.path.exists(rf_model_path) and os.path.exists(xgb_model_path):
    # Ask the user if they want to retrain the models
    if ask_for_retraining():
        perform_training = True
    else:
        print(f'\n{Fore.GREEN}Using pre-trained models!{Style.RESET_ALL}')
else:
    # If models do not exist, training starts automatically
    perform_training = True

# Run training if required
if perform_training:
    run_training()

# Ask the user if they want to perform model evaluation
if ask_for_evaluation():
    perform_evaluation = True

# If evaluation is requested, perform analysis on the evaluation set
if perform_evaluation:

    evaluation_folder_path = os.path.join(main_folder_path, 'evaluation set')

    if not os.path.exists(evaluation_folder_path):
        print(f'\n{Fore.RED}Evaluation folder not found: {evaluation_folder_path}{Style.RESET_ALL}')
        sys.exit(1)

    # Create test set folder
    output_evaluation_folder_path = os.path.join(evaluation_folder_path, 'evaluation_results')

    # Create the output folder if it doesn't exist
    os.makedirs(output_evaluation_folder_path, exist_ok=True)

    print(f'\n{Fore.YELLOW}Starting evaluation for folder:{Style.RESET_ALL} {main_folder_name}{Fore.YELLOW} with delta = {Style.RESET_ALL}{delta}')
    classification_results = evaluate_user_scenarios(evaluation_folder_path, delta)

    print(f'\n{Fore.GREEN}Evaluation successfully completed!{Style.RESET_ALL}')

    if classification_results == {} or classification_results is None:
        print(f'\n{Fore.RED}No classification results available!{Style.RESET_ALL}')
    else:
        # Write evaluation results to the output file
        write_window_results(output_evaluation_folder_path, main_folder_name, delta, classification_results)
else:
    print(f'\n{Fore.GREEN}Operation finished without model evaluation.{Style.RESET_ALL}')
import os
import sys
from colorama import Fore, Style
from sklearn.model_selection import train_test_split
from classifier_module import train_and_evaluate_classifier
from dataset_formatter import read_dataset_files

# Get dataset folder path from command line
if len(sys.argv) < 3:
    print(f'\n{Fore.RED}ERROR: You must provide a dataset folder path and a dataset type as command line arguments!{Style.RESET_ALL}')
    print(f'{Fore.YELLOW}Usage: python {sys.argv[0]} <dataset folder path> <dataset type>{Style.RESET_ALL}')
    sys.exit(1)

# Dataset folder path and name
main_folder_path = str(sys.argv[1])
main_folder_name = main_folder_path.split('/')[-1]

# Output folder path
output_folder_path = f'{os.path.dirname(main_folder_path)}/{main_folder_name}/classification_results/'

# If argv[2] is PingPong it means we are dealing with a double dataset (PingPong in this case), and we must train the model with
# the "standalone" folder and test it with the "smarthome" one
if str(sys.argv[2]).lower() == 'distinct_sets':

    # Start the analysis of the datasets
    print(f'\n{Fore.YELLOW}Starting analysis for folder: {Style.RESET_ALL}{main_folder_name}')

    # read data from training dataset
    X_train, y_train = read_dataset_files(f'{main_folder_path}/standalone', f'{main_folder_name}/standalone')

    # read data from test dataset
    X_test, y_test = read_dataset_files(f'{main_folder_path}/smarthome', f'{main_folder_name}/smarthome')

    # Train and evaluate the classifier
    print(f'\n{Fore.MAGENTA}Training and evaluating the classifier...{Style.RESET_ALL}')

    accuracy, report = train_and_evaluate_classifier(X_train, y_train, X_test, y_test)

elif str(sys.argv[2]).lower() == 'unified_set':

    # Start the analysis of the dataset
    print(f'\n{Fore.YELLOW}Starting analysis for folder: {Style.RESET_ALL}{main_folder_name}')

    # Read data from dataset (The same dataset is used to train and test the model)
    X, y = read_dataset_files(main_folder_path, main_folder_name)

    # Split the dataset into training and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=None)

    # Train and evaluate the classifier
    print(f'\n{Fore.MAGENTA}Training and evaluating the classifier...{Style.RESET_ALL}')

    accuracy, report = train_and_evaluate_classifier(X_train, y_train, X_test, y_test)

else:
    print(f'\n{Fore.RED}ERROR: Dataset type not valid!{Style.RESET_ALL}')
    sys.exit(1)

# Create the output folder if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Write results to the output file
with open(f'{output_folder_path}/{main_folder_name}_results.txt', 'w') as file:

    print(f'\n{Fore.YELLOW}Writing results for folder: {Style.RESET_ALL}{main_folder_name}')

    # Write results to file
    file.write(f'Results for folder {main_folder_name} are:\n')
    file.write(f'\nAccuracy: {accuracy:.3f}\n')
    file.write(f'\nClassification Report: \n\n{report}')

    print(f'\n{Fore.GREEN}Results successfully written!{Style.RESET_ALL}')

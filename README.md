# Network IoT Traffic Classifier

## Project Description

This project aims to analyze and classify network flows captured from Internet of Things (IoT) devices. The primary goal is to develop a classification model that can accurately categorize different activities or behaviors exhibited by these devices based on network traffic data. The analysis involves processing packet captures (.pcap files) and associated timestamps to extract features, which are then used to train a Random Forest classifier.

## Dataset used for the implementation:
* Pingpong Dataset: https://athinagroup.eng.uci.edu/projects/pingpong/data/
* Bhosale Dataset (link of the paper): https://www.scitepress.org/Papers/2021/104765/104765.pdf

## Project Structure

The project is organized into the following files:

- **main.py**: Main script to execute the classification process.
- **classifier_module.py**: Random Forest classifier implementation.
- **dataset_formatter.py**: Dataset formatting functions.
- **flow_labeling.py**: Flow labeling functions.
- **ip_addresses.py**: IP address mapping functions.
- **utilities.py**: Utility functions for IP address extraction, timestamp conversion and statistical feature computation.

## Modules

### 1. Utilities Module (utilities.py)

This module provides utility functions for various tasks, including converting timestamps, filtering packets based on timestamps and computing statistical features from packet lengths.

### 2. Classifier Module (classifier_module.py)

The classifier module implements a Random Forest classifier. It includes a function to train and evaluate the classifier both for a dataset with a unified set of data and a dataset with two distinct sets of data. The module also showcases the use of cross-validation and scaling features.

### 3. Dataset Formatting Module (dataset_formatter.py)

This module is responsible for reading dataset files, including .pcap and .timestamps files. It extracts features from packet flows, combines them with corresponding labels and prepares the data for training the classifier. The module includes functions to read .timestamps files, read .pcap files and format the overall dataset.

### 4. Flow Labeling Module (flow_labeling.py)

The flow labeling module provides functions for classifying activities based on labels and indices obtained from timestamps. It assigns integer labels to different IoT device activities, allowing for easier interpretation and analysis of the classification results.

### 5. IP Addresses Module (ip_addresses.py)

The IP Addresses module provides a function to map device names to their corresponding IP addresses. This is useful for identifying the source and destination of network traffic flows.

## Results

The classification results, including accuracy and a detailed classification report, are saved in the output folder. The output file is named `<dataset_name>_results.txt` and contains the following information:

- Accuracy of the classifier.
- Classification Report, including precision, recall and F1-score for each class.

## Dependencies

The project relies on the following Python libraries:

- **Colorama**: A Python library for adding color to terminal text.
- **NumPy**: A library for numerical operations in Python.
- **Pandas**: A data manipulation library.
- **Scapy**: A library for capturing, crafting and sending network packets.
- **Scikit-learn**: A machine learning library for Python.

These libraries must be installed in the Python environment before running the project.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ldklab/netpolicy.git
    cd network_IoT_traffic_classifier
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1. **Dataset Preparation**: Ensure your dataset is organized with subfolders for each device containing both .pcap and .timestamps files.

2. **Run Classifier**: Execute the main script to train and evaluate the Random Forest classifier. Specify the dataset folder path and name as command-line arguments.


   ```bash
   python main.py <dataset_folder_path> <dataset_type>
    ```

   - Values allowed for <dataset_type> are: "unified_set" or "distinct_sets":
     
     - `unified_set`: with the read pcap files, a single feature matrix will be created. That matrix will then be split into training and test sets according to the following proportions: 75% for training set and 25% for test set;
     - `distinct_sets`: with the read pcap files, two distinct feature matrices will be created. One matrix will be used for training the model, while the other one will be used for testing it;

## Main Functions

### `read_dataset_files(folder_path, folder_name)`

This function iterates over all the files in the given directory, identifies pcap (`.pcap`) and timestamps (`.timestamps`) files and reads their contents. It then returns two NumPy arrays that are used as data and target for the classifier.

#### Parameters:
- `folder_path` (str): The path to the folder containing pcap and timestamps files.
- `folder_name` (str): The name of the folder containing the dataset.

#### Returns:
- `dataset_features` (numpy.ndarray): NumPy array (matrix) representing the features for the classifier.
- `dataset_labels` (numpy.ndarray): NumPy array representing the class labels associated with the features.

### `get_ip_address(device_name)`

This function returns the IP address associated with the device name passed as a parameter.

#### Parameters:
- `device_name` (str): The name of the device.

#### Returns:
- `ip_address` (list): A list of IP addresses associated with the device name. Returns -1 if no matching IP address is found.

### `get_flow_label(activity, index)`

This function returns the label associated with the activity passed as a parameter.

#### Parameters:
- `activity` (str): The activity coming from the type of captured flow.
- `index` (int): Indicates whether the flow is associated with the Toggle-ON or Toggle-OFF of the activity, according to the timestamp.

#### Returns:
- `label` (int): The integer label associated with the activity.

### `train_and_evaluate_classifier(X_train, y_train, X_test, y_test)`

Trains a Random Forest classifier using the training set and evaluates its performance using the test set.

#### Parameters:
- `X_train` (numpy.ndarray): Array-like or matrix of shape (n_samples, n_features) representing the features from the training set of the dataset.
- `y_train` (numpy.ndarray): Array-like of shape (n_samples) representing the class labels associated with the features in X from the training set of the dataset.
- `X_test` (numpy.ndarray): Array-like or matrix of shape (n_samples, n_features) representing the features from the test set of the dataset.
- `y_test` (numpy.ndarray): Array-like of shape (n_samples) representing the class labels associated with the features in X from the test set of the dataset.

#### Returns:
- `accuracy` (float): The accuracy of the classifier.
- `report` (str): The classification report.

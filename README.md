# Network IoT Traffic Classifier

## Project Description

This project aims to analyze and classify network flows captured from Internet of Things (IoT) devices. The primary goal is to develop classification models that can accurately detect different activities performed by these devices, only based on their network traffic. The pipeline involves capturing network traffic, extracting statistical features from .pcapng files using activity timestamps and training two machine learning models (Random Forest and XGBoost) to recognize patterns.

The system supports both training and evaluation phases, and it has been tested on realistic usage scenarios involving two smart home IoT devices.

## Dataset used for the implementation:

* ENSF 619 IoT Dataset: https://osf.io/zf8pm/files/osfstorage

It contains network captures and activity timestamps from two IoT devices (Sonos Smart Speaker and TP-Link Tapo Smart Camera) under several user activities: 
camera and speaker startup, speaker play music and volume adjustment, camera call and video stream. 

The dataset is organized into:

- A **training / test set** directory used for model development.
- An **evaluation set** directory simulating real user behavior for testing model generalization.

## Project Structure

The project is organized into the following components:

- `main.py`: Main script to execute the training, testing and (optional) evaluation phases.
- `training_test_modules/`:
  - `classifier_module.py`: Contains functions to train and test both Random Forest and XGBoost classifiers.
  - `dataset_formatter.py`: Functions to parse, format and extract features from raw traffic.
- `evaluation_modules/`:
  - `evaluation_module.py`: Implements the evaluation logic on the user scenarios.
  - `evaluation_utilities.py`: Contains utility functions for the evaluation phase.
- `common_modules/`:
  - `flow_labeling.py`: Functions to assign labels to activities based on timestamps.
  - `ip_addresses.py`: Maps device names to IP addresses.
  - `utilities.py`: Helper functions for timestamp parsing, packet filtering and feature computation.

## Functionality

- **Automatic training**: If no model files are found, both classifiers are trained and the models saved.
- **Model reuse**: If trained models exist, the user is asked whether to reuse or retrain them.
- **Optional evaluation**: After training or detecting existing models, the user can choose to run an evaluation on realistic traffic.

## Training / Test Results

Results are saved in the `classification_results/` folder. Each output file (e.g., `training_<dataset_name>_<delta>_results.txt`) includes:

- Classifier accuracy
- Full classification report (precision, recall, F1-score)

## Evaluation Results

The evaluation results are saved in the `evaluation_results/` folder. Each output file (e.g., `evaluation_<dataset_name>_<delta>_results.txt`) includes:

- Name of the files evaluated
- Window start and end timestamps
- Classifiers predictions

## Dependencies

The project requires the following Python packages:

- `colorama`
- `numpy`
- `pandas`
- `scapy`
- `scikit-learn`
- `xgboost`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Francesco-rosati/elements_of_software_security_project.git
   cd elements_of_software_security_project
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
## How to Use

1. Organize your dataset in the following structure:

   ```
   dataset_folder/
   ├── training - test set/
   │   ├── <device_1>/
   │   │   ├── device_traffic.pcapng
   │   │   └── timestamps.txt
   │   └── ...
   └── evaluation set/
       ├── traffic_scenario.pcapng
       └── ...
   ```
   
2. Run the main script:

   ```bash
   python main.py <dataset_folder_path>
   ```

   - `<dataset_folder_path>`: Path to the folder containing the dataset (e.g., `./dataset`)

## Main Functions Overview

### `read_training_files(folder_path, folder_name, delta)`

Reads `.pcapng` and `.timestamps` files, extracts features within `delta` seconds of activity start and returns the feature matrix and label array.

---

### `train_and_test_rf_classifier(X_train, y_train, X_test, y_test, delta)`

Trains a Random Forest model and returns accuracy and a full classification report.

---

### `train_and_test_xgb_classifier(X_train, y_train, X_test, y_test, delta)`

Trains an XGBoost model and returns accuracy and a classification report.

---

### `def evaluate_user_scenarios(folder_path, delta)`

Applies both trained classifiers to the evaluation set and outputs the classification performance over realistic user behavior.

---

### `get_flow_label(activity)`

Assigns and returns an integer label to a device activity based on its name.

---

### `get_ip_address(device_name)`

Returns the IP address associated with the given device name.

---

### `window_packets(packets, delta, overlap=2)`

Filters packets within a specified time window (`delta`) and overlap to create a list of packets for each activity.
It returns a list of windows, each containing a list of packets.

---

## Notes

- `delta` is the analysis window used to extract features around each activity timestamp.
- `overlap` represents the number of seconds to overlap between consecutive windows, and it has to be lower than `delta`.
- The model performance varies depending on the delta value. Typical values include: `20s`, `10s`, `5s`, `1s`, etc.
- Each model is saved under:
  - `rf_models/trained_rf_classifier_<delta>.pkl`
  - `xgb_models/trained_xgb_classifier_<delta>.pkl`
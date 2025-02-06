# shallow_resilience
This repository is the code basis for the paper entitled "Rethinking Security: The Resilience of Shallow ML Models]{Rethinking Security: The Resilience of Shallow ML Models"
It explores several security threads directed toward ML models using the applied scenario of a captcha service.

## Experiments

To run the experiments, the first step is to generate the datasets. To do so, the script `generate_datasets.py` is needed.
When executing the script, the most important flags are the `--behavior`, which defines how the evil bots
will work, and the `-v`, which controls how many votes the system takes before making a decision towards 
a label. To define the output folder, use the `-o` flags.

After the dataset is generated to train the models on the different subsets of data, use the `run_ml.py`.
The necessary flags to run the script are the `-i` that define in which dataset the models will be trained.
Usually, the output folder of the previous script. The output folder can be controlled using the `-o` flag.

## Files

The `datasets.py` defines the Dataset class used during dataset generation. 
It has methods to provide a captcha, store the answer and write the to files in batches.

The `convert_dataset.py` transforms the raw data in `ubyte` to `.csv` format.

The bots folder contains the bots with different behaviors. 
The `good` bot always answers correctly, and the `evil` bot always answers incorrectly with three behavior available (random, switch, and flip).

The process results folder provides tools to analyze the outputs from the `run_ml` file.

The `plot_ml_data.py` creates a 3D plot of the model's performance in the file provided.
The `merge_results.py` merges the results obtained for the same model in different attacks to enable an easier comparison.
The `get_results.py` provides a statistical analysis of the results, pinpointing when a model drops below a performance threshold and the worst and best performance per model.

# Results 

## Model breaking point

### No voting system

#### Random attack

Model     |Data point   |% Malicious Users |  Dataset Size |  % of dataset |
| -- | --- |---|--| -- |  
LR        |[ 7,  2]     |0.35              |  26400        |  0.11         |  
SVM       |[ 7,  2]     |0.35              |  26400        |  0.11         |  
KNN(1)    |[12,  3]     |0.60              |  30600        |  0.25         |  
KNN(3)    |[14,  5]     |0.70              |  39000        |  0.38         |  
KNN(5)    |[17,  7]     |0.85              |  47400        |  0.53         |  
KNN(7)    |[18,  8]     |0.90              |  51600        |  0.59         |  
KNN(9)    |[18,  9]     |0.90              |  55800        |  0.61         |  
DT        |[11,  1]     |0.55              |  22200        |  0.10         |  
ANN       |[15,  6]     |0.75              |  43200        |  0.44         |  
RF        |[--, --]     |--                |  --           |  --           |  
VF(hard)  |[16,  6]     |0.80              |  43200        |  0.47         |  
VF(soft)  |[13,  5]     |0.65              |  39000        |  0.35         |

#### Switch attack

Model     | Data point |  % Malicious Users |  Dataset Size |  % of dataset |  
| -- | --- |---|--| -- |  
LR        | [10,  2]   |  0.50              |  26400        |  0.16         |  
SVM       | [ 9,  2]   |  0.45              |  26400        |  0.14         |  
KNN(1)    | [12,  3]   |  0.60              |  30600        |  0.25         |  
KNN(3)    | [13,  4]   |  0.65              |  34800        |  0.31         |  
KNN(5)    | [13,  5]   |  0.65              |  39000        |  0.35         |  
KNN(7)    | [14,  5]   |  0.70              |  39000        |  0.38         |  
KNN(9)    | [15,  5]   |  0.75              |  39000        |  0.40         |  
DT        | [ 8,  2]   |  0.40              |  26400        |  0.13         |  
ANN       | [14,  5]   |  0.70              |  39000        |  0.38         |  
RF        | [15,  6]   |  0.75              |  43200        |  0.44         |  
VF(hard)  | [15,  5]   |  0.75              |  39000        |  0.40         |  
VF(soft)  | [11,  2]   |  0.55              |  26400        |  0.17   |

#### Flip attack

Model     |Data point  | % Malicious Users  | Dataset Size |  % of dataset   |
| -- | --- |---|--| -- |  
LR        |[ 7,  2]    | 0.35               | 26400        |  0.11           |
SVM       |[ 8,  2]    | 0.40               | 26400        |  0.13           |
KNN(1)    |[12,  3]    | 0.60               | 30600        |  0.25           |
KNN(3)    |[13,  4]    | 0.65               | 34800        |  0.31           |
KNN(5)    |[13,  5]    | 0.65               | 39000        |  0.35           |
KNN(7)    |[14,  5]    | 0.70               | 39000        |  0.38           |
KNN(9)    |[15,  5]    | 0.75               | 39000        |  0.40           |
DT        |[ 8,  2]    | 0.40               | 26400        |  0.13           |
ANN       |[14,  5]    | 0.70               | 39000        |  0.38           |
RF        |[15,  6]    | 0.75               | 43200        |  0.44           |
VF(hard)  |[14,  5]    | 0.70               | 39000        |  0.38           |
VF(soft)  |[13,  2]    | 0.65               | 26400        |  0.21     |

### Mitigation system - 3 votes

#### Random attack

Model     | Data point  | % Malicious Users   |Dataset Size  | % of dataset |  
| -- | --- |---|--| -- |
LR        | [11,  4]    | 0.55                |34800         | 0.27         |  
SVM_linear| [12,  4]    | 0.60                |34800         | 0.29         |  
KNN(1)    | [15,  6]    | 0.75                |43200         | 0.44         |  
KNN(3)    | [17,  6]    | 0.85                |43200         | 0.50         |  
KNN(5)    | [18,  8]    | 0.90                |51600         | 0.59         |  
KNN(7)    | [19,  8]    | 0.95                |51600         | 0.62         |  
KNN(9)    | [18, 10]    | 0.90                |60000         | 0.63         |  
DT        | [12,  4]    | 0.60                |34800         | 0.29         |  
ANN       | [17,  8]    | 0.85                |51600         | 0.55         |  
RF        | [--, --]    | --                  |--            | --           |  
VF(hard)  | [18,  6]    | 0.90                |43200         | 0.53         |  
VF(soft)  | [17,  4]    | 0.85                |34800         | 0.41    |

#### Switch attack

Model     |Data point  | % Malicious Users  | Dataset Size  | % of dataset   |
| -- | --- |---|--| -- |
LR        |[ 9,  2]    | 0.45               | 26400         | 0.14           |
SVM_linear|[11,  1]    | 0.55               | 22200         | 0.10           |
KNN(1)    |[12,  3]    | 0.60               | 30600         | 0.25           |
KNN(3)    |[13,  4]    | 0.65               | 34800         | 0.31           |
KNN(5)    |[13,  5]    | 0.65               | 39000         | 0.35           |
KNN(7)    |[14,  5]    | 0.70               | 39000         | 0.38           |
KNN(9)    |[15,  5]    | 0.75               | 39000         | 0.40           |
DT        |[ 8,  2]    | 0.40               | 26400         | 0.13           |
ANN       |[14,  5]    | 0.70               | 39000         | 0.38           |
RF        |[15,  6]    | 0.75               | 43200         | 0.44           |
VF(hard)  |[15,  6]    | 0.75               | 43200         | 0.44           |
VF(soft)  |[12,  3]    | 0.60               | 30600         | 0.25           |

#### Flip attack

Model     | Data point  | % Malicious Users  | Dataset Size  | % of dataset  |
| -- | --- |---|--| -- | 
LR        | [10,  2]    | 0.50               | 26400         | 0.16          | 
SVM_linear| [ 7,  2]    | 0.35               | 26400         | 0.11          | 
KNN(1)    | [12,  3]    | 0.60               | 30600         | 0.25          | 
KNN(3)    | [13,  4]    | 0.65               | 34800         | 0.31          | 
KNN(5)    | [13,  5]    | 0.65               | 39000         | 0.35          | 
KNN(7)    | [14,  5]    | 0.70               | 39000         | 0.38          | 
KNN(9)    | [14,  5]    | 0.70               | 39000         | 0.38          | 
DT        | [11,  1]    | 0.55               | 22200         | 0.10          | 
ANN       | [14,  5]    | 0.70               | 39000         | 0.38          | 
RF        | [15,  6]    | 0.75               | 43200         | 0.44          | 
VF(hard)  | [15,  4]    | 0.75               | 34800         | 0.36          | 
VF(soft)  | [11,  3]    | 0.55               | 30600         | 0.23    |


### Mitigation system - 5 votes

#### Random attack

Model     | Data point |  % Malicious Users |  Dataset Size |  % of dataset   |
| -- | --- |---|--| -- | 
LR        | [15,  6]   |  0.75              |  43200        |  0.44           |
SVM_linear| [15,  4]   |  0.75              |  34800        |  0.36           |
KNN(1)    | [17,  6]   |  0.85              |  43200        |  0.50           |
KNN(3)    | [17,  8]   |  0.85              |  51600        |  0.55           |
KNN(5)    | [18,  8]   |  0.90              |  51600        |  0.59           |
KNN(7)    | [19,  8]   |  0.95              |  51600        |  0.62           |
KNN(9)    | [19, 10]   |  0.95              |  60000        |  0.67           |
DT        | [15,  5]   |  0.75              |  39000        |  0.40           |
ANN       | [17,  8]   |  0.85              |  51600        |  0.55           |
RF        | [--, --]   |  --                |  --           |  --             |
VF(hard)  | [17,  8]   |  0.85              |  51600        |  0.55           |
VF(soft)  | [17,  6]   |  0.85              |  43200        |  0.50     |

#### Switch attack

Model     | Data point  | % Malicious Users |  Dataset Size |  % of dataset   |
| -- | --- |---|--| -- | 
LR        | [ 7,  2]    | 0.35              |  26400        |  0.11           |
SVM_linear| [11,  1]    | 0.55              |  22200        |  0.10           |
KNN(1)    | [12,  3]    | 0.60              |  30600        |  0.25           |
KNN(3)    | [14,  4]    | 0.70              |  34800        |  0.34           |
KNN(5)    | [13,  5]    | 0.65              |  39000        |  0.35           |
KNN(7)    | [14,  5]    | 0.70              |  39000        |  0.38           |
KNN(9)    | [15,  5]    | 0.75              |  39000        |  0.40           |
DT        | [ 8,  2]    | 0.40              |  26400        |  0.13           |
ANN       | [14,  5]    | 0.70              |  39000        |  0.38           |
RF        | [15,  6]    | 0.75              |  43200        |  0.44           |
VF(hard)  | [15,  6]    | 0.75              |  43200        |  0.44           |
VF(soft)  | [11,  3]    | 0.55              |  30600        |  0.23           |


#### Flip attack

Model     |Data point  | % Malicious Users |  Dataset Size |  % of dataset |  
| -- | --- |---|--| -- | 
LR        |[ 9,  2]    | 0.45              |  26400        |  0.14         |  
SVM_linear|[ 9,  2]    | 0.45              |  26400        |  0.14         |  
KNN(1)    |[12,  3]    | 0.60              |  30600        |  0.25         |  
KNN(3)    |[14,  4]    | 0.70              |  34800        |  0.34         |  
KNN(5)    |[13,  5]    | 0.65              |  39000        |  0.35         |  
KNN(7)    |[14,  5]    | 0.70              |  39000        |  0.38         |  
KNN(9)    |[15,  5]    | 0.75              |  39000        |  0.40         |  
DT        |[ 8,  2]    | 0.40              |  26400        |  0.13         |  
ANN       |[13,  5]    | 0.65              |  39000        |  0.35         |  
RF        |[15,  6]    | 0.75              |  43200        |  0.44         |  
VF(hard)  |[14,  5]    | 0.70              |  39000        |  0.38         |  
VF(soft)  |[13,  2]    | 0.65              |  26400        |  0.21         |  

### Mitigation system - 7 votes

#### Random attack

Model     |Data point |  % Malicious Users |  Dataset Size |  % of dataset |  
| -- | --- |---|--| -- | 
LR        |[16,  5]   |  0.80              |  39000        |  0.43         |  
SVM_linear|[16,  4]   |  0.80              |  34800        |  0.39         |  
KNN(1)    |[17,  5]   |  0.85              |  39000        |  0.46         |  
KNN(3)    |[18,  7]   |  0.90              |  47400        |  0.56         |  
KNN(5)    |[19,  6]   |  0.95              |  43200        |  0.55         |  
KNN(7)    |[19,  8]   |  0.95              |  51600        |  0.62         |  
KNN(9)    |[19, 10]   |  0.95              |  60000        |  0.67         |  
DT        |[16,  5]   |  0.80              |  39000        |  0.43         |  
ANN       |[18,  9]   |  0.90              |  55800        |  0.61         |  
RF        |[--, --]   |  --                |  --           |  --           |  
VF(hard)  |[18,  9]   |  0.90              |  55800        |  0.61         |  
VF(soft)  |[18,  6]   |  0.90              |  43200        |  0.53         |

#### Switch attack

Model     | Data point  | % Malicious Users |  Dataset Size |  % of dataset |  
| -- | --- |---|--| -- | 
LR        | [ 7,  2]    | 0.35              |  26400        |  0.11         |  
SVM_linear| [ 9,  2]    | 0.45              |  26400        |  0.14         |  
KNN(1)    | [12,  3]    | 0.60              |  30600        |  0.25         |  
KNN(3)    | [14,  4]    | 0.70              |  34800        |  0.34         |  
KNN(5)    | [14,  5]    | 0.70              |  39000        |  0.38         |  
KNN(7)    | [14,  5]    | 0.70              |  39000        |  0.38         |  
KNN(9)    | [15,  5]    | 0.75              |  39000        |  0.40         |  
DT        | [ 8,  2]    | 0.40              |  26400        |  0.13         |  
ANN       | [14,  5]    | 0.70              |  39000        |  0.38         |  
RF        | [15,  6]    | 0.75              |  43200        |  0.44         |  
VF(hard)  | [15,  5]    | 0.75              |  39000        |  0.40         |  
VF(soft)  | [11,  3]    | 0.55              |  30600        |  0.23         |  


#### Flip attack

Model     | Data point |  % Malicious Users |  Dataset Size |  % of dataset |  
| -- | --- |---|--| -- | 
LR        | [11,  2]   |  0.55              |  26400        |  0.17         |  
SVM_linear| [ 7,  2]   |  0.35              |  26400        |  0.11         |  
KNN(1)    | [12,  3]   |  0.60              |  30600        |  0.25         |  
KNN(3)    | [14,  4]   |  0.70              |  34800        |  0.34         |  
KNN(5)    | [13,  5]   |  0.65              |  39000        |  0.35         |  
KNN(7)    | [14,  5]   |  0.70              |  39000        |  0.38         |  
KNN(9)    | [14,  5]   |  0.70              |  39000        |  0.38         |  
DT        | [ 8,  2]   |  0.40              |  26400        |  0.13         |  
ANN       | [15,  4]   |  0.75              |  34800        |  0.36         |  
RF        | [15,  6]   |  0.75              |  43200        |  0.44         |  
VF(hard)  | [15,  5]   |  0.75              |  39000        |  0.40         |  
VF(soft)  | [11,  3]   |  0.55              |  30600        |  0.23         |  

## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)
* **Rafael Teixeira** - [rgtzths](https://github.com/rgtzths)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

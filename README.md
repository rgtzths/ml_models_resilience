# shallow_resilience
This repository is the code basis for the paper entitled "Data Poisoning: When ML feels ill."
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

## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)
* **Rafael Teixeira** - [rgtzths](https://github.com/rgtzths)
* **Rafael Simões** - []()
* **Vitor Cunha** - []()

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

# Results 

Since the results are three-dimensional plots, they are presented on the GitHub pages.

To check them, click [here](https://rgtzths.github.io/shallow_resilience/).

# gliberal-lightsheet-2023

This repository contains all code part of the work entitled "Open top multi sample dual view light sheet microscope for live imaging of large multicellular systems".
Below you will find installation instructions as well as ways how to test the code with example data.

## Installation instructions

To utilize the scripts is is recommended to create a virtual environment. this can be done with e.g. [conda](https://docs.conda.io/en/latest/miniconda.html) or [vitualenv](https://docs.python.org/3/library/venv.html).
After creating the environment you will need to install following packages:

```pip install scipy==1.10.0 seaborn==0.12.2 pandas==1.5.3 tifffile==2021.7.2 cikit-image==0.20.0.dev0 numpy==1.23.5 matplotlib==3.7.0 dipy==1.7.0```

This will take approximately 2.5 min depending on the machine you use.

## Example usage

You can try the example data present in the example folder. There is prepared example outputs present in the /ExampleData/Output/ folder.
The expected runtime on normal desktop computers (around 16GB of RAM and 16 cores) depends on the script used and ranges up to 30 min for the registration step.
To run the scripts on your own acquired data, you just need to change the `path_data` and `path_save` variables in each script.

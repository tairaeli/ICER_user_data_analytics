**Project: ICER User Data Analytics**

This document provides instructions for setting up the environment, installing necessary packages, and running demo code for the ICER User Data Analytics project. Follow these steps to ensure a smooth setup.

**Prerequisites**

- Ensure you have git installed on your system to clone the repository.

- Download and install [Miniconda](https://docs.anaconda.com/free/miniconda/). for your operating system from the Miniconda website. This will be used to manage the project's environment and dependencies.

**Cloning the Repository**

1. Open a terminal or command prompt.

2. Clone the project repository using the following command:
   
```bash
git clone https://github.com/tairaeli/ICER_user_data_analytics.git
```

3. Navigate into the project directory:

```bash
cd ICER_user_data_analytics
```

**Dependencies**

Once in the package directory, there are several methods to ensure that all of the depedencies are installed properly on your device:

1. Using Conda 

If you are a conda user, you can use the following code in the project's main directory

```bash
conda env create --file ./environment.yml
conda activate user_dat_analysis
```

2. Manual Installation

This project uses mostly relies on many popular, well-maintained packages, so a manual installation is quite simple. All you need to do is to make sure all of the following packages are installed:
- numpy
- scikit-learn
- matplotlib
- pandas
- seaborn

**Data Instructions**

Since the project does not include large datasets in the repository, please follow the instructions provided by the project team or instructors to obtain the necessary data. Place this data in the data directory located at the root of the project repository. Use relative paths in your code to access this data to ensure portability.

**Running the Demo**

1. Start JupyterLab or Jupyter Notebook:
   
```bash
jupyter lab
```


Or:

```bash
jupyter notebook
```

2. Open the demo notebook file (demo.ipynb) located in the main project directory. This notebook contains example code demonstrating the use of the software, including data preprocessing, analysis, and visualization techniques.

**Troubleshooting**

- If you encounter any issues related to UTF8 errors on Windows, run the following command in your git repository directory to ensure the correct encoding:

```bash
conda env export --from-history | Set-Content -Encoding utf8 environment.yml
```

**Support**

For any issues or questions, please refer to the contacts of the project maintainers.


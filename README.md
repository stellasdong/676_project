# Comorbidity Pattern Mining and Cost Prediction in Texas Inpatient Hospital Data

**Author:** Stella Dong  
*Department of Computer Science & Engineering, Texas A&M University*  
*CSCE 676: Data Mining and Analysis — Prof. James Caverlee*


## Project Video

**[Watch the project video here](https://youtu.be/3f_2MJME-no)**


## Overview

This project investigates whether comorbidity patterns in Texas inpatient hospital records can reveal clinically meaningful patient subgroups and predict high-cost visits. Using 2019 inpatient discharge data from Bryan–College Station (BCS) area facilities, patient diagnoses are mapped from raw ICD-10-CM codes to standardized CCSR categories and analyzed via association rule mining (Apriori), UMAP dimensionality reduction, and K-Medoids clustering. The result is a two-stage clustering pipeline that uncovers eight clinically coherent patient subgroups, which are then used alongside demographic features to predict whether a visit falls in the top quartile of charges. This work demonstrates that comorbidity structure is a meaningful but partial signal for cost prediction, with comorbidity count and subgroup membership ranking among the top predictors alongside patient age.

## Main Notebook

**The main deliverable is [main_notebook.ipynb](main_notebook.ipynb)**

This single notebook contains the full pipeline: data loading and cleaning, ICD-10-CM to CCSR mapping, exploratory co-occurrence analysis, association rule mining, clustering (K-Medoids + UMAP), sub-clustering, and cost prediction models.

## Research Questions

1. Can we define distinct patient subgroups in the BCS inpatient population?

2. Which comorbidity subgroups are the strongest predictors of high inpatient charges?


## Data

**Dataset:** [Texas DSHS Inpatient Public Use Data File (PUDF)](https://www.dshs.texas.gov/center-health-statistics/texas-health-care-information-collection/download-and-purchase-data/texas-inpatient-public-use-data-file-pudf/public-use-data-File-pudf-inpatient-free-download)

The statewide Texas PUDF was pre-filtered to retain only inpatient discharge records from the **6 Bryan–College Station reporting facilities** that submitted data across all four quarters of 2019. The resulting file `bcs_tx_inpatient.csv` is **not included in this repository** due to size; it is loaded from Google Drive in the notebook.

**Preprocessing steps (all performed in `main_notebook.ipynb`):**
1. Load the pre-filtered BCS CSV
2. Map each of the up to 25 ICD-10-CM diagnosis columns to a CCSR category via the `icd-mappings` package
3. Filter sparse CCSR features (< 5% prevalence) before clustering
4. Binary-encode the per-visit CCSR set into a multi-hot matrix for downstream modeling

**Auxiliary file:** `ccsr_descriptions.txt` — human-readable labels for CCSR codes, sourced from the [HCUP CCSR reference](https://hcup-us.ahrq.gov/toolssoftware/ccsr/DXCCSR-vs-Beta-CCS-Comparison.xlsx)

### Loading the Data

To reproduce the exact BCS dataset used in this project:

1. Go to the [Texas DSHS Inpatient PUDF page](#data) and click **Agree** to accept the usage conditions.
2. Under **2019**, download the **Tab-delimited file** for all 4 quarters of the year.
3. Extract each zip file. Inside each, locate the file named `PUDF_base1_Xq2019_tab.txt` (where `X` is 1–4).
4. Create a folder (e.g. `pudf/`) and move all four `.txt` files into it.
5. Open [`extract_bcs_tx_inpatient.py`](extract_bcs_tx_inpatient.py) and set `DATA_PATH` at the top to your folder's path:
   ```python
   DATA_PATH = "pudf"  # path to folder containing the four PUDF .txt files
   ```
6. Run the script:
   ```bash
   python extract_bcs_tx_inpatient.py
   ```
   This produces `bcs_tx_inpatient.csv` in the current directory, containing only records from the Bryan–College Station area facilities.


## Reproducing the Work

This project was built and run on **Google Colab**. To reproduce:

1. Clone this repository
2. Upload `main_notebook.ipynb` to Google Colab (or open it via Google Drive)
3. Place `bcs_tx_inpatient.csv` and `ccsr_descriptions.txt` at paths accessible to the notebook (update `DATA_PATH` and `CCSR_DESC_PATH` in the first code cell to match your Drive/Colab paths)
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run all cells in `main_notebook.ipynb` from top to bottom — the notebook is fully self-contained

> **Note:** UMAP fitting on the full dataset can take several minutes per dimensionality setting.

## Key Dependencies

| Package | Version |
|---|---|
| Python | 3.10+ (Google Colab default) |
| pandas | ≥ 2.0, < 3 |
| numpy | < 2 |
| scikit-learn | 1.6.1 |
| umap-learn | 0.5.12 |
| scipy | 1.13.1 |
| numba | 0.60.0 |
| icd-mappings | 0.5.0 |
| mlxtend | ≤ 0.23.1 |
| hdbscan | latest |
| scikit-learn-extra | latest |
| matplotlib | ≥ 3.8 |
| seaborn | ≥ 0.13 |

The full pinned dependency list lives in [`requirements.txt`](requirements.txt).

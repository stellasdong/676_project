# Comorbidity Pattern Mining and Cost Prediction in Texas Inpatient Hospital Data

**Author:** Stella Dong  
*Department of Computer Science & Engineering, Texas A&M University*  
*CSCE 676: Data Mining and Analysis — Prof. James Caverlee*


## Project Video

**[Watch the project video here](https://youtu.be/3f_2MJME-no)**


## Overview

This project investigates whether comorbidity patterns in Texas inpatient hospital records can reveal clinically meaningful patient subgroups and predict high-cost visits. Using 2019 inpatient discharge data from Bryan–College Station (BCS) area facilities, patient diagnoses are mapped from raw ICD-10-CM codes to standardized CCSR categories and analyzed via association rule mining (Apriori), UMAP dimensionality reduction, and K-Medoids clustering. The result is a two-stage clustering pipeline that uncovers eight clinically coherent patient subgroups, which are then used alongside demographic features to predict whether a visit falls in the top quartile of charges. This work demonstrates that comorbidity structure is a meaningful but partial signal for cost prediction, with comorbidity count and subgroup membership ranking among the top predictors alongside patient age.

## Main Notebook

> ### 👉 Start here: [main_notebook.ipynb](main_notebook.ipynb)

This single notebook contains the full pipeline: data loading and cleaning, ICD-10-CM to CCSR mapping, exploratory co-occurrence analysis, association rule mining, clustering (K-Medoids + UMAP), sub-clustering, and cost prediction models.

## Research Questions

1. Can we define distinct patient subgroups in the BCS inpatient population?

2. Which comorbidity subgroups are the strongest predictors of high inpatient charges?

## Results Summary

A two-stage clustering pipeline (UMAP 5D + K-Medoids, k=4, silhouette=0.75 then sub-clustering the adult group at UMAP 10D + K-Medoids k=5, silhouette=0.70) yields **eight clinically coherent subgroups**: 

The first stage separates the various maternal and neonatal inpatient visits:

| Cluster | Label | n | % | Defining Profile |
|---------|-------|---|-------|------------------|
| 0 | **Neonatal Inpatients** | 1,072 | 8.8% | Sick or at-risk newborns requiring dedicated care. |
| 1 | **General Adult Comorbidities** | 9,049 | 74.3% | Broad chronic-disease mix: administrative/status codes, hypertension, lipid disorders, coronary disease, obesity, depression, CKD, heart failure, diabetes. Heterogeneous — sub-clustered further below. |
| 2 | **Obstetric / Labor & Delivery** | 1,547 | 12.7% | Largely near-universal gestational-weeks and maternal delivery-outcome codes with childbirth complications, perineal trauma, and malposition as secondary codes. Homogeneous maternal admissions. |
| 3 | **Healthy Newborn Encounters** | 511 | 4.2% | Mostly universal infectious-disease screening and liveborn, jaundice as the only notable secondary code. Routine well-newborn visits with minimal additional diagnoses. |

Then, cluster 1 is re-embedded and partitioned independently, revealing five distinct chronic-disease subgroups:

| Sub-cluster | Label | n | % of Cluster 1 | Defining Profile |
|-------------|-------|---|---------------------|------------------|
| 1 | **Mixed Psychiatric & Substance Use** | 1,511 | 16.7% | Depressive disorders, anxiety, bipolar, schizophrenia spectrum, suicidal ideation/self-harm, alcohol-related, cannabis-related. Predominantly mental-health and substance-use admissions with mild medical comorbidity. |
| 2 | **Severe Cardiorenal-Metabolic Disease** | 2,992 | 33.1% | Hypertension with complications, chronic kidney disease, heart failure, coronary atherosclerosis, diabetes with complications, cardiac dysrhythmias, aplastic anemia. The highest-burden chronic-disease group. |
| 3 | **General Cardiometabolic & Musculoskeletal** | 4,250 | 47.0% | Essential hypertension, lipid disorders, obesity, osteoarthritis, coronary disease, anxiet. Broad but lower-severity chronic conditions typical of general adult admissions. |
| 4 | **Pure Depressive Disorder** | 167 | 1.8% | Depressive disorders in 99.4% of patients with virtually no other comorbiditie. |
| 5 | **Schizophrenia Spectrum (Isolated)** | 129 | 1.4% | Schizophrenia spectrum in 100% of patients with negligible secondary diagnoses. |

Comorbidity subgroups are meaningful but partial predictors of high charges (top-quartile threshold): the strongest features are comorbidity count (~35–40% of Random Forest importance) and patient age (~30–37%), with Logistic Regression achieving ROC-AUC **0.732** and Random Forest **0.705**.

## Data

**Dataset:** [Texas DSHS Inpatient Public Use Data File (PUDF)](https://www.dshs.texas.gov/center-health-statistics/texas-health-care-information-collection/download-and-purchase-data/texas-inpatient-public-use-data-file-pudf/public-use-data-File-pudf-inpatient-free-download)

The statewide Texas PUDF was pre-filtered to retain only inpatient discharge records from the **6 Bryan–College Station reporting facilities** that submitted data across all four quarters of 2019. The resulting file `bcs_tx_inpatient.csv` is **not included in this repository** due to size; it is loaded from Google Drive in the notebook.

**Preprocessing steps (all performed in `main_notebook.ipynb`):**
1. Load the pre-filtered BCS CSV
2. Map each of the up to 25 ICD-10-CM diagnosis columns to a CCSR category via the `icd-mappings` package
3. Filter sparse CCSR features (< 5% prevalence) before clustering
4. Binary-encode the per-visit CCSR set into a multi-hot matrix for downstream modeling

**Auxiliary file:** `data/ccsr_descriptions.txt` — human-readable labels for CCSR codes, sourced from the [HCUP CCSR reference](https://hcup-us.ahrq.gov/toolssoftware/ccsr/DXCCSR-vs-Beta-CCS-Comparison.xlsx)

### Loading the Data

To reproduce the exact BCS dataset used in this project:

1. Go to the [Texas DSHS Inpatient PUDF page](#data) and click **Agree** to accept the usage conditions.
2. Under **2019**, download the **Tab-delimited file** for all 4 quarters of the year.
3. Extract each zip file. Inside each, locate the file named `PUDF_base1_Xq2019_tab.txt` (where `X` is 1–4).
4. Create a folder (e.g. `pudf/`) and move all four `.txt` files into it.
5. Open [`scripts/extract_bcs_tx_inpatient.py`](scripts/extract_bcs_tx_inpatient.py) and set `DATA_PATH` at the top to your folder's path:
   ```python
   DATA_PATH = "pudf"  # path to folder containing the four PUDF .txt files
   ```
6. Run the script:
   ```bash
   python scripts/extract_bcs_tx_inpatient.py
   ```
   This produces `bcs_tx_inpatient.csv` in the current directory, containing only records from the Bryan–College Station area facilities.


## Reproducing the Work

This project was built and run on **Google Colab**. To reproduce:

1. Clone this repository
2. Upload `main_notebook.ipynb` to Google Colab (or open it via Google Drive)
3. Place `bcs_tx_inpatient.csv` and `data/ccsr_descriptions.txt` at paths accessible to the notebook (update `DATA_PATH` and `CCSR_DESC_PATH` in the first code cell to match your Drive/Colab paths)
4. Install dependencies (requires **Python 3.10+**):
   ```bash
   pip install -r requirements.txt
   ```
5. Run all cells in `main_notebook.ipynb` from top to bottom — the notebook is fully self-contained

> **Note:** UMAP fitting on the full dataset can take several minutes per dimensionality setting.

## Repository Structure

```
676_project/
├── main_notebook.ipynb     # full pipeline — main deliverable
├── requirements.txt        # pinned Python dependencies
├── checkpoints/            # graded checkpoint submissions
│   ├── checkpoint_1.ipynb
│   └── checkpoint_2.ipynb
├── scripts/
│   └── extract_bcs_tx_inpatient.py  # filters raw PUDF .txt files to BCS subset
└── data/
    └── ccsr_descriptions.txt        # CCSR code to human-readable label reference
```

## Key Dependencies

| Package | Version |
|---|---|
| Python | 3.10+ |
| pandas | 2.3.3 |
| numpy | 1.26.4 |
| scikit-learn | 1.6.1 |
| umap-learn | 0.5.12 |
| scipy | 1.13.1 |
| numba | 0.60.0 |
| icd-mappings | 0.5.0 |
| mlxtend | 0.23.1 |
| scikit-learn-extra | 0.3.0 |
| matplotlib | 3.9.4 |

The full pinned dependency list lives in [`requirements.txt`](requirements.txt).

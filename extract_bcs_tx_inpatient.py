import pandas as pd
import numpy as np

# UPDATE: set this to the folder containing the four PUDF_base1_Xq2019_tab.txt files
DATA_PATH = "pudf"

tx_inpatient_q1 = pd.read_csv(f"{DATA_PATH}/PUDF_base1_1q2019_tab.txt", sep="\t", low_memory=False)
tx_inpatient_q2 = pd.read_csv(f"{DATA_PATH}/PUDF_base1_2q2019_tab.txt", sep="\t", low_memory=False)
tx_inpatient_q3 = pd.read_csv(f"{DATA_PATH}/PUDF_base1_3q2019_tab.txt", sep="\t", low_memory=False)
tx_inpatient_q4 = pd.read_csv(f"{DATA_PATH}/PUDF_base1_4q2019_tab.txt", sep="\t", low_memory=False)

tx_inpatient = pd.DataFrame(
    np.concatenate([
        tx_inpatient_q1.values,
        tx_inpatient_q2.values,
        tx_inpatient_q3.values,
        tx_inpatient_q4.values,
    ]),
    columns=tx_inpatient_q1.columns,
)

BCS_THCIC_ID = ["975162", "975270", "717500", "002001", "206100", "975403", "976329"]
tx_inpatient["THCIC_ID"] = tx_inpatient["THCIC_ID"].astype(str)
bcs_tx_inpatient = tx_inpatient[tx_inpatient["THCIC_ID"].isin(BCS_THCIC_ID)]

output_path = "bcs_tx_inpatient.csv"
bcs_tx_inpatient.to_csv(output_path, index=False)
print(f"Saved {len(bcs_tx_inpatient)} rows to {output_path}")

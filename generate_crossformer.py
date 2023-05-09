# the prediction will be saved in ./results/{setting}/generated.csv
import numpy as np
import pandas as pd
np.set_printoptions(suppress=True)

setting = "Crossformer_Netflow_il168_ol24_sl6_win2_fa10_dm256_nh4_el3_itr0" # chagne this to the setting name
df_raw = pd.read_csv("./datasets/updated_urg16.csv") #change this to the dataset path

cols = list(df_raw.columns); cols.remove('date') # ['date'] from cols
print("the columns in output, ", cols)

prediction = np.load('./results/'+setting+'/pred.npy')
print("the shape of the prediction", prediction.shape)

prediction_length = prediction.shape[1]
i = 0
df = pd.DataFrame(columns = cols)

# Append the entire dataset to the generated.csv
while i < prediction.shape[0]: 
    df = pd.concat([df, pd.DataFrame(prediction[i,], columns = cols)], ignore_index=True)

    i = i + prediction_length

print(df.head(5))
df.to_csv('./results/' + setting + '/generated.csv', sep='\t')
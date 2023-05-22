# the prediction will be saved in ./results/{setting}/generated.csv
import numpy as np
import pandas as pd
import torch as torch

setting = "Crossformer_Entire_Netflow_il168_ol24_sl6_win2_fa10_dm256_nh4_el3_itr0" # chagne this to the setting name
df_raw = pd.read_csv("./datasets/updated_categorical_urg16.csv") #change this to the dataset path
one_hot = pd.get_dummies(data=df_raw, columns=['proto', 'type'], dtype=float) # Get one-hot encoding of variable

df_raw = df_raw.drop(columns=['date', 'proto', 'type']) # remove ['date'] from cols

cols = list(df_raw.columns); 
# print("the columns in output: ", cols)
# print("the dtypes in output: ", df_raw.dtypes)

np.set_printoptions(suppress=True,
                    formatter={'float_kind':'{:0.5f}'.format})  # suppress scientific notation 

prediction = np.load('./results/'+setting+'/pred.npy')
# print("the shape of the prediction", prediction.shape)

# print(prediction[0,1,:])

prediction_length = prediction.shape[1]
i = 0

pd.set_option('display.float_format', lambda x: '%.5f' % x) # suppress scientific notation 
df = pd.DataFrame(columns = cols)

# Append the entire dataset to the generated.csv
while i < prediction.shape[0]: 

    # continous 
    new_df = pd.DataFrame(prediction[i,:,:8], columns = cols)
    
    # categorical ('proto')
    proto_labels = one_hot.columns[9:16].tolist()
    tensors = torch.from_numpy(prediction[i,:,8:15])

    maxIdx = torch.argmax(tensors, axis=1)
    ret = []
    for j in range(len(maxIdx)):
        label = proto_labels[maxIdx[j]]
        ret.append(label.removeprefix('proto_'))

    new_df['proto'] = ret

    # categorical ('type')
    type_labels = one_hot.columns[16:17].tolist()
    tensors = torch.from_numpy(prediction[i,:,15:16])

    maxIdx = torch.argmax(tensors, axis=1)
    ret = []
    for j in range(len(maxIdx)):
        label = type_labels[maxIdx[j]]
        ret.append(label.removeprefix('type_'))
    
    new_df['type'] = ret
    
    df = pd.concat([df, new_df], ignore_index=True)
    i = i + prediction_length

# print(df.head(5))
df.to_csv('./results/' + setting + '/generated.csv', sep='\t')
# Crossformer: Transformer Utilizing Cross-Dimension Dependency for Multivariate Time Series Forecasting (ICLR 2023)

This is the origin Pytorch implementation of [Crossformer: Transformer Utilizing Cross-Dimension Dependency for Multivariate Time Series Forecasting](https://openreview.net/forum?id=vSVLM2j9eie).

## Generate Synthetic Network Trace Data based on the Crossformer MTSF 

### Dataset 
* caida pcap 
* urg16 netflow 

### Pre-process data (Optional)

* pcap 
```
python pcap-converter.py
```

* netflow 

```
python netflow-converter.py
```

if want to include categorical dataset:
```
python netflow-categorical-converter.py
```


### Step 1: Train/Validation for Forecasting 

* netflow 
```
python main_crossformer.py --data Netflow --data_path updated_urg16.csv --data_dim 8 --in_len 168 --out_len 24 --seg_len 6
```

if want to include categorical dataset:
```
python main_crossformer.py --data Entire_Netflow --data_path updated_categorical_urg16.csv --data_dim 17 --in_len 168 --out_len 24 --seg_len 6
```

* pcap 

```
python main_crossformer.py --data PCAP --data_path updated_pcap.csv --data_dim 11 --in_len 168 --out_len 24 --seg_len 6
```

### Step 1: Train/Validation for Generation 


* netflow 
```
python main_crossformer.py --data Netflow --data_path updated_urg16.csv --data_dim 8 --in_len 1 --out_len 1 --seg_len 6
```

if want to include categorical dataset:
```
python main_crossformer.py --data Entire_Netflow --data_path updated_categorical_urg16.csv --data_dim 17 --in_len 1 --out_len 1 --seg_len 6
```

* pcap 

```
python main_crossformer.py --data PCAP --data_path updated_pcap.csv --data_dim 11 --in_len 1 --out_len 1 --seg_len 6
```


### Step 2: Evaluation for Forecasting

* netflow 

```
python eval_crossformer.py --setting_name Crossformer_Netflow_il168_ol24_sl6_win2_fa10_dm256_nh4_el3_itr0 --save_pred --inverse
```

if want to include categorical dataset:
```
python eval_crossformer.py --setting_name Crossformer_Entire_Netflow_il168_ol24_sl6_win2_fa10_dm256_nh4_el3_itr0  --save_pred --inverse
```

* pcap 
```
python eval_crossformer.py --setting_name Crossformer_PCAP_il168_ol24_sl6_win2_fa10_dm256_nh4_el3_itr0 --save_pred --inverse
```

### Step 2: Evaluation for Generation 

* netflow 

```
python eval_crossformer.py --setting_name Crossformer_Netflow_il1_ol1_sl6_win2_fa10_dm256_nh4_el3_itr0 --save_pred --inverse
```

if want to include categorical dataset:
```
python eval_crossformer.py --setting_name Crossformer_Entire_Netflow_il1_ol1_sl6_win2_fa10_dm256_nh4_el3_itr0  --save_pred --inverse
```

* pcap 
```
python eval_crossformer.py --setting_name Crossformer_PCAP_il1_ol1_sl6_win2_fa10_dm256_nh4_el3_itr0 --save_pred --inverse
```

### Step 3: Synthetic data generation (Post-process) -- only for generation 

* netflow/pcap -- please change the `generate_crossformer.py` accordingly. 

```
python generate_crossformer.py
```

* netflow with categorical features 

```
python generate_netflow_categorical_crossformer.py
```

To view the csv file, 
```
cat results/Crossformer_Netflow_il1_ol1_sl6_win2_fa10_dm256_nh4_el3_itr0/generated.csv | column -t -s, | less -S
```

```
cat results/Crossformer_PCAP_il1_ol1_sl6_win2_fa10_dm256_nh4_el3_itr0/generated.csv | column -t -s, | less -S
```

```
cat results/Crossformer_Entire_Netflow_il1_ol1_sl6_win2_fa10_dm256_nh4_el3_itr0/generated.csv | column -t -s, | less -S
```


## Custom Usage
We use the [AirQuality](https://archive.ics.uci.edu/ml/machine-learning-databases/00360/AirQualityUCI.zip) dataset to show how to train and evaluate Crossformer with your own data. 

1. Modify the `AirQualityUCI.csv` dataset into the following format, where the first column is date (or you can just leave the first column blank) and the other 13 columns are multivariate time series to forecast. And put the modified file into folder `datasets/`
<p align="center">
<img src=".\pic\Data_format.PNG" height = "120" alt="" align=center />
<br>
<b>Figure 4.</b> An example of the custom dataset.
</p>

2. This is an hourly-sampled dataset with 13 dimensions. And we are going to use the past week (168 hours) to forecast the next day (24 hour) and the segment length is set to 6. Therefore, we need to run:
```
python main_crossformer.py --data AirQuality --data_path AirQualityUCI.csv --data_dim 13 --in_len 168 --out_len 24 --seg_len 6
```

3. We can evaluate the trained model by running:
```
python eval_crossformer.py --setting_name Crossformer_AirQuality_il168_ol24_sl6_win2_fa10_dm256_nh4_el3_itr0 --save_pred
```
The model will be evaluated, predicted and ground truth series will be saved in `results/Crossformer_AirQuality_il168_ol24_sl6_win2_fa10_dm256_nh4_el3_itr0`


`main_crossformer` is the entry point of our model and there are other parameters that can be tuned. Here we describe them in detail:
| Parameter name | Description of parameter |
| --- | --- |
| data           | The dataset name                                             |
| root_path      | The root path of the data file (defaults to `./datasets/`)    |
| data_path      | The data file name (defaults to `ETTh1.csv`)                  |
| data_split | Train/Val/Test split, can be ratio (e.g. `0.7,0.1,0.2`) or number (e.g. `16800,2880,2880`), (defaults to `0.7,0.1,0.2`) 
| checkpoints    | Location to store the trained model (defaults to `./checkpoints/`)  |
| in_len | Length of input/history sequence, i.e. $T$ in the paper (defaults to 96) |
| out_len | Length of output/future sequence, i.e. $\tau$ in the paper (defaults to 24) |
| seg_len | Length of each segment in DSW embedding, i.e. $L_{seg}$ in the paper (defaults to 6) |
| win_size | How many adjacent segments to be merged into one in segment merging of HED  (defaults to 2) |
| factor | Number of routers in Cross-Dimension Stage of TSA, i.e. $c$ in the paper (defaults to 10) |
| data_dim | Number of dimensions of the MTS data, i.e. $D$ in the paper (defaults to 7 for ETTh and ETTm) |
| d_model | Dimension of hidden states, i.e. $d_{model}$ in the paper (defaults to 256) |
| d_ff | Dimension of MLP in MSA (defaults to 512) |
| n_heads | Num of heads in MSA (defaults to 4) |
| e_layers | Num of encoder layers, i.e. $N$ in the paper (defaults to 3) |
| dropout | The probability of dropout (defaults to 0.2) |
| num_workers | The num_works of Data loader (defaults to 0) |
| batch_size | The batch size for training and testing (defaults to 32) |
| train_epochs | Train epochs (defaults to 20) |
| patience | Early stopping patience (defaults to 3) |
| learning_rate | The initial learning rate for the optimizer (defaults to 1e-4) |
| lradj | Ways to adjust the learning rate (defaults to `type1`) |
| itr | Experiments times (defaults to 1) |
| save_pred | Whether to save the predicted results. If True, the predicted results will be saved in folder `results` in numpy array form. This will cost a lot time and memory for datasets with large $D$. (defaults to `False`). |
| use_gpu | Whether to use gpu (defaults to `True`) |
| gpu | The gpu no, used for training and inference (defaults to 0) |
| use_multi_gpu | Whether to use multiple gpus (defaults to `False`) |
| devices | Device ids of multile gpus (defaults to `0,1,2,3`) |

## Citation
If you find this repository useful in your research, please cite:
```
@inproceedings{
zhang2023crossformer,
title={Crossformer: Transformer Utilizing Cross-Dimension Dependency for Multivariate Time Series Forecasting},
author={Yunhao Zhang and Junchi Yan},
booktitle={International Conference on Learning Representations},
year={2023},
}
```


## Acknowledgement
We appreciate the following works for their valuable code and data for time series forecasting:

https://github.com/zhouhaoyi/Informer2020

https://github.com/thuml/Autoformer

https://github.com/alipay/Pyraformer

https://github.com/MAZiqing/FEDformer

The following two Vision Transformer works also inspire our DSW embedding and HED designs:

https://github.com/google-research/vision_transformer

https://github.com/microsoft/Swin-Transformer

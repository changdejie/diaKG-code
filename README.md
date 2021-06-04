## train model
```
please set appropriate batch_size
python trainer.py --data_dir entity_type_data --bert_config models/chinese_roberta_wwm_large_ext_pytorch --batch_size 16 --max_epochs 10 --gpus 1
```
## evaluate model
```
python evaluate.py 

```
## compute different entity info
```
datasets/compute_acc_linux.py or datasets/compute_acc.py

```

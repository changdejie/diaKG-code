# A Unified MRC Framework for Named Entity Recognition 
The repository contains the code of the recent research advances in [Shannon.AI](http://www.shannonai.com). 

**A Unified MRC Framework for Named Entity Recognition** <br>
Xiaoya Li, Jingrong Feng, Yuxian Meng, Qinghong Han, Fei Wu and Jiwei Li<br>
In ACL 2020. [paper](https://arxiv.org/abs/1910.11476)<br>
If you find this repo helpful, please cite the following:
```latex
@article{li2019unified,
  title={A Unified MRC Framework for Named Entity Recognition},
  author={Li, Xiaoya and Feng, Jingrong and Meng, Yuxian and Han, Qinghong and Wu, Fei and Li, Jiwei},
  journal={arXiv preprint arXiv:1910.11476},
  year={2019}
}
```
For any question, please feel free to post Github issues.<br>

## Install Requirements
`pip install -r requirements.txt`

We build our project on [pytorch-lightning.](https://github.com/PyTorchLightning/pytorch-lightning)
If you want to know more about the arguments used in our training scripts, please 
refer to [pytorch-lightning documentation.](https://pytorch-lightning.readthedocs.io/en/latest/)

## Prepare Datasets
You can [download](./ner2mrc/download.md) our preprocessed MRC-NER datasets or 
write your own preprocess scripts. We provide `ner2mrc/mrsa2mrc.py` for reference.

## Prepare Models
For English Datasets, we use [BERT-Large](https://github.com/google-research/bert)

For Chinese Datasets, we use [RoBERTa-wwm-ext-large](https://github.com/ymcui/Chinese-BERT-wwm)

## Train
The main training procedure is in `trainer.py`

Examples to start training are in `scripts/reproduce`.

Note that you may need to change `DATA_DIR`, `BERT_DIR`, `OUTPUT_DIR` to your own
dataset path, bert model path and log path, respectively.

## Evaluate
`trainer.py` will automatically evaluate on dev set every `val_check_interval` epochs,
and save the topk checkpoints to `default_root_dir`.

To evaluate them, use `evaluate.py`

# 模型经改造后使用如下
## 训练模型
```
训练的时候依据自己的机器情况设置参数，参数过大容易导致显存溢出
python trainer.py --data_dir entity_type_data --bert_config models/chinese_roberta_wwm_large_ext_pytorch --batch_size 16 --max_epochs 10 --gpus 1
```
## 评估模型
```
需要修改evaluate里面新模型的路径
python evaluate.py 

```
## 统计详细不同实体信息
```
datasets/compute_acc_linux.py or datasets/compute_acc.py

```

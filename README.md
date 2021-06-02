
# DiaKG: an Annotated Diabetes Dataset for Medical Knowledge Graph Construction

This is the source code of the DiaKG [paper](https://arxiv.org/abs/2105.15033).

## DataSet 

### Overview
The DiaKG dataset is derived from 41 diabetes guidelines and consensus, which are from authoritative Chinese journals including basic research, clinical research, drug usage, clinical cases, diagnosis and treatment methods, etc. The dataset covers the most extensive field of research content and hotspot in recent years. The annotation process is done by 2 seasoned endocrinologists and 6 M.D. candidates, and finally conduct a high-quality diabates database which contains 22,050 entities and 6,890 relations in total.

### Get the Data
The codebase only provides some sample annotation files. If you want to download the fullset, please apply at [Tianchi Platform](https://tianchi.aliyun.com/dataset/dataDetail?dataId=88836).

### Data Format
The dataset is exhibited as a hierachical structure with "document-paragraph-sentence" information. All the entities and sentences are labelled on the sentence level. Below is an example:

```
{ 
  "doc_id": "1", // string, document id 
  "paragraphs": [ // array, paragraphs 
    {
      "paragraph_id": "0", // string, paragraph id
      "paragraph": "中国成人2型糖尿病胰岛素促泌剂应用的专家共识", // string, paragraph text
      "sentences": [ // array, sentences
        {
          "sentence_id": "0", // string, sentence id
          "sentence": "中国成人2型糖尿病胰岛素促泌剂应用的专家共识", // string, sentence text
          "start_idx": 0, // int, sentence start index in the current paragraph
          "end_idx": 22, // int, sentence end index in the current paragraph
          "entities": [ // array, entities in the current sentence
            {
              "entity_id": "T0", // string, entity id
              "entity": "2型糖尿病", // string, entity text
              "entity_type": "Disease", // string, entity type
              "start_idx": 4, // int, entity start index in the sentence
              "end_idx": 9 // int, entity end index in the sentence
            },
            {
              "entity_id": "T1",
              "entity": "2型",
              "entity_type": "Class",
              "start_idx": 4,
              "end_idx": 6
            },
            {
              "entity_id": "T2",
              "entity": "胰岛素促泌剂",
              "entity_type": "Drug",
              "start_idx": 9,
              "end_idx": 15
            }
          ],
          "relations": [ // array, relations in the current sentence
            {
              "relation_type": "Drug_Disease", // string, relation type
              "relation_id": "R0", // string, relation id
              "head_entity_id": "T2", // string, head entity id
              "tail_entity_id": "T0" // string, tail entity id
            },
            {
              "relation_type": "Class_Disease",
              "relation_id": "R1",
              "head_entity_id": "T1",
              "tail_entity_id": "T0"
            }
          ]
        }
      ]
    },
    {
      "paragraph_id": "1", // string, paragraph id
      "paragraph": "xxx" // string, paragraph text
      "sentences": [
        ...
      ] 
    },
    ...
  ] 
}
```

### Data Statistic

#### Entity

@请栋栋补充

| Entity | Freq | Fraction(%) | Avg Length |
|-----|-----------|------------|----------|
| Disease | xx | xx | xx |
| Total | | | |

#### Relation

@请利平补充

| Relation | Freq | Fraction(%) | Avg Cross-sentence Number |
|-----|-----------|------------|----------|
|Drug_Disease| xx | xx | xx |
|Total| | | |

* Note: **Avg Cross-sentence Number** means the average sentences that the two entities that compose a relation locate, since the annotation is conducted on document level and cross-sentence relation is allowed.
 
## Experiments

### NER

@请栋栋补充

We use [MRC-BERT](web link) as our baseline model, and the source code is in the **NER** directory.

#### How to run
```
cd NER

## Training:
python trainer.py --data_dir entity_type_data --bert_config models/chinese_roberta_wwm_large_ext_pytorch --batch_size 16 --max_epochs 10 --gpus 1

## Inference:
python evaluate.py 

```

#### Results
把论文中的实验结果全部都copy到这里吧，论文仅列出了5条结果


### RE

@请利平补充

We use [Bi-directional GRU-Attention](link) as our baseline model, and the source code is in the **RE** directory.

#### How to run
```
cd RE

## Training:

## Inference:

```

#### Results
同NER实验要求

## Citation

If you use DiaKG in your research, please cite our [paper](https://arxiv.org/abs/2105.15033):
```
@article{chang2021diakg,
      title={DiaKG: an Annotated Diabetes Dataset for Medical Knowledge Graph Construction}, 
      author={Dejie Chang and Mosha Chen and Chaozhen Liu and Liping Liu and Dongdong Li and Wei Li and Fei Kong and Bangchang Liu and Xiaobin Luo and Ji Qi and Qiao Jin and Bin Xu},
      journal={arXiv preprint arXiv:2105.15033}，
      year={2021}
  }
```

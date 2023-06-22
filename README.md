# ___LinSNPGT: Genotyping of specified SNP sites on linux system___


### LinSNPGT requires :
  - Python >= 3.7 
  - bowtie2 
  - samtools
  - java8

### Installing
Clone LinSNPGT

```
git clone git@github.com:JessieChen7/LinSNPGT.git --recursive

cd LinSNPGT

virtualenv -p python3 cactus_env
```

## 💡 General Introduction
We have developed a toolkit to call variant loci on the windows system, [**WinSNPGT**](https://github.com/JessieChen7/WinSNPGT), which is very friendly to those who have little experience in linux operation. It can obtain the genotypes of the raw sequencing data for the snp loci specified in our datasets. LinSNPGT is the Linux platform version of this toolkit. The installation and use of this toolkit is described below.

## 📘 Table of Contents

- Background
- Change Log
- Data
- Installation
- Usage
- Frequently Asked Questions
- Contacts

## 🧾 Background
We have developed a phenotype prediction platform, **[CropGStools](http://iagr.genomics.cn/CropGS/#/)**, which contains multiple high-quality datasets from important crops such as rice, maize and so on. These datasets were used as training sets to build models for phenotype prediction. Users can upload genotypes of their own samples to the platform for online phenotype prediction.

The LinSNPGT toolkit was developed to ensure that the genotypes uploaded by users match those in the training set for modeling so that bias in the prediction results can be avoided. Users can run this program on the linux system to realize the whole process from sequencing files to getting genotypes by simple operation.

## 🔍 Change Log
- [Version 1.0](https://github.com/JessieChen7/LinSNPGT) -First version released on June, 1st, 2023

## 🔍 Data
The example-data files are not included in the release package, you can download [example-data.tar.gz](https://figshare.com/articles/dataset/WinSNPGT_example_data/23365061) and extract data with command `tar zxvf example-data.tar.gz`.

The species of the example-data files is *Oryza sativa*, you can select the rice-related dataset in the toolkit to complete the genotyping.
## 🌟 Installation


## 🌟 Usage


The output format is like:

\#CHROM|POS|Line1|line2
---|---|---|---
1|1077|T|T
1|12127|G|G
...|...|...|...
10|1299332|T|A
10|1299513|G|G
...|...|...|...

---
The following step-by-step notes may help you more clearly understand the use of the program:



## 💡 Frequently Asked Questions
If there are some errors reported during the running of the program, please refer to the following scenarios to solve the problem:



The above are some possible causes of errors, if there are any other problems, welcome to contact us.

## 👥 Contacts
Jie Qiu (qiujie@shnu.edu.cn)  
Min Zhu (1185643615@qq.com)  
Jiaxin (jxchen1217@gmail.com)



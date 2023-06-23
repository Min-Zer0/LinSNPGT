# ___LinSNPGT: Genotyping of specified SNP sites on linux system___

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
### LinSNPGT requires :
  - __Python__
  - __bowtie2__ 
  - __samtools__
  - __[java8](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)__
  - If you want to use __SNPGT-build__, you will also need to install __seqtk__

### Installing
```
git clone https://github.com/JessieChen7/LinSNPGT.git
cd LinSNPGT
chmod +x ./install.sh && ./install

# install java8
./Install.Java8.sh

# install bowtie2
sudo apt install bowtie2

# install samtools
sudo apt install samtools

# install seqtk
sudo apt-get install seqtk
```

## 🌟 SNPGT
There are three subfolders and tree files after the package is unziped.

- **.sys**
- **01.Reference_Genome**
- **02.Input_Fastq**
- `makeRef.py`
- `SNPGT.config`
- `SNPGT.py`

To run LinSNPGT via `SNPGT.py`, you need to fill in the `SNPGT.config` and put files in the corresponding path.

Here are the steps:

1. Fill in the `config.txt` file
	- Generally, the Software Path does not need to be changed.

 	- Project_Name: Enter your project name which will be output file prefix.	 
	- RefDataSetFile: Enter your dataset corresponding to the model to be fitted.
		- It must follow the format './01.Reference_Genome/`*.tar.gz`'
		- Available species and datasets are listed below the `config.txt` file, including their download links.
		- The species of the RefDataSet should match your raw sequencing data.
	- Thread_Count: Enter the number of threads available to run the program
	- Samples_list: Fill in your raw sequencing data and their corresponding sample names.
		- It must follow the format '|SAMPLE NAME|RAW READS NAME|RAW READS NAME'
		- It should be vertical-bar-separated, with each sample represented on a separate row and each reads file represented in a separate column.
### Example
```
#=================== Software Path =======================#
Java_Path=./jdk/bin/java
Bowtie2_Path=bowtie2
Samtools_Path=samtools
#=========================================================#

#=================== LinSNPGT Config =======================#
* [Project]
Project_Name=Rice.TEST

* [Species and Dataset]
RefDataSetFile=./Reference_Genome/Rice_378_Inbred.tar.gz

* [Running LinSNPGT Thread]
Thread_Count=10

* [Samples_list]
> |sample|Read1|Read2|
| Line1 | TEST1_r1.fastq | TEST1_r2.fastq |
| Line2 | TEST2_r1.fastq | TEST2_r2.fastq |
#===========================================================#
```

2. Download the RefDataSetFile file  `(*.tar.gz)` and move it to the path: **./01.Reference_Genome** 
3. Move your raw sequencing data `(*.fastq.gz)` or `(*.fastq)` to the path: **./02.Input_Fastq**
4. run the command: `python SNPGT.py`

The output file is in the 0000.00.00.result directory
The output format is like:

\#CHROM|POS|Line1
---|---|---
Chr1|128960|A
Chr1|133137|C
...|...|...
Chr12|321216|A
Chr12|364257|A
Chr12|364755|.
...|...|...

## 🌟 Make Ref

`python makeRef.py -h`

```
usage: makeRef.py [-h] [-F FASTA] [-B BIM] [-S SPECIES] [-N STRAIN] [-L BINLEN] [--JavaPath JAVAPATH] [--SamtoolsPath SAMTOOLSPATH] [--SeqtkPath SEQTKPATH]
                  [--Bowtie2Path BOWTIE2PATH]

SNPGT-build (Tools for make RefGenome)

optional arguments:
  -h, --help            show this help message and exit
  -F FASTA, --fasta FASTA
                        Whole genome reference sequence
  -B BIM, --bim BIM     SNP site information(bim file)
  -S SPECIES, --species SPECIES
                        Specify species name; eg. Rice
  -N STRAIN, --strain STRAIN
                        Specify strain name; eg. 378_Inbred
  -L BINLEN, --binlen BINLEN
                        The simplified of the genome retains base length on both sides of the SNP. The default value is 400
  --JavaPath JAVAPATH   Path to java8. The default is ./jdk/bin/java
  --SamtoolsPath SAMTOOLSPATH
                        Path to samtools.
  --SeqtkPath SEQTKPATH
                        Path to Seqtk.
  --Bowtie2Path BOWTIE2PATH
                        Path to bowtie2-build.
```

### Example
`python makeRef.py -F path_to/Rice.fa -B path_to/R378_Inbred.bim -S Rice -N 378_Inbre`

## 💡 Frequently Asked Questions
If there are some errors reported during the running of the program, please refer to the following scenarios to solve the problem:



The above are some possible causes of errors, if there are any other problems, welcome to contact us.

## 👥 Contacts
Jie Qiu (qiujie@shnu.edu.cn)  
Min Zhu (1185643615@qq.com)  
Jiaxin (jxchen1217@gmail.com)



# ___LinSNPGT: Genotyping of specified SNP sites on Linux system___

## 💡 General Introduction
We have developed a toolkit to call variant loci on the windows system, [**WinSNPGT**](https://github.com/Min-Zer0/WinSNPGT), which is very friendly to those who have little experience in linux operation. It can obtain the genotypes of the raw sequencing data for the snp loci specified in our datasets. LinSNPGT is the Linux platform version of this toolkit. The installation and use of this toolkit is described below.

## 🧾 Background
We have developed a phenotype prediction platform, **[CropGStools](https://iagr.genomics.cn/CropGS/#/)**, which contains multiple high-quality datasets from important crops such as rice, maize and so on. These datasets were used as training sets to build models for phenotype prediction. Users can upload genotypes of their own samples to the platform for online phenotype prediction.

The LinSNPGT toolkit was developed to ensure that the genotypes uploaded by users match those in the training set for modeling so that bias in the prediction results can be avoided. Users can run this program on the linux system to realize the whole process from sequencing files to getting genotypes by simple operation.

## 🔍 Data
The example-data files are not included in the release package, you can download [example-data.tar.gz](https://figshare.com/articles/dataset/WinSNPGT_example_data/23365061) and extract data with command `tar zxvf example-data.tar.gz`.

The species of the example-data files is *Oryza sativa*, you can select the rice-related dataset (e.g: GSTP007 ~ GSTP009) in the toolkit to complete the genotyping.

In the process of using LinSNPGT, you need to download RefDataSetFile. Listed below is the download link and RefDataSet_File name that needs to be filled in the `config.txt` file.

- Maize (*Zea mays*):
	- [GSTP001_8652_Hybrid](https://iagr.genomics.cn/static/gstool/data/GSTP001/SNPGT/Maize_8652_Hybrid.tar.gz) : Maize_8652_Hybrid
	- [GSTP002_5820_Hybrid](https://iagr.genomics.cn/static/gstool/data/GSTP002/SNPGT/Maize_5820_Hybrid.tar.gz) : Maize_5820_Hybrid
	- [GSTP003_1458_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP003/SNPGT/Maize_1458_Inbred.tar.gz) : Maize_1458_Inbred
	- [GSTP004_1404_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP004/SNPGT/Maize_1404_Inbred.tar.gz) : Maize_1404_Inbred
	- [GSTP005_350_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP005/SNPGT/Maize_350_Inbred.tar.gz) : Maize_350_Inbred
	- [GSTP006_1604_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP006/SNPGT/Maize_1604_Inbred.tar.gz) : Maize_1604_Inbred
- Rice (*Oryza sativa*):
	- [GSTP007_1495_Hybrid](https://iagr.genomics.cn/static/gstool/data/GSTP007/SNPGT/Rice_1495_Hybrid.tar.gz) : Rice_1495_Hybrid
	- [GSTP008_705_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP008/SNPGT/Rice_705_Inbred.tar.gz) : Rice_705_Inbred
	- [GSTP009_378_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP009/SNPGT/Rice_378_Inbred.tar.gz) : Rice_378_Inbred
- Cotton (*Gossypium hirsutum*):
	- [GSTP010_1245_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP0010/SNPGT/Cotton_1245_Inbred.tar.gz) : Cotton_1245_Inbred
- Millet (*Setaria italica*):
	- [GSTP011_827_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP0011/SNPGT/Millet_827_Inbred.tar.gz) : Millet_827_Inbred
- Chickpea (*Cicer arietinum*):
	- [GTP012_2921_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP0012/SNPGT/Chickpea_2921_Inbred.tar.gz) : Chickpea_2921_Inbred
- Rapeseed (*Brassica napus*):
	- [GSTP013_991_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP0013/SNPGT/Rapeseed_991_Inbred.tar.gz) : Rapeseed_991_Inbred
- Soybean (*Glycine max*):
	- [GSTP014_2795_Inbred](https://iagr.genomics.cn/static/gstool/data/GSTP0014/SNPGT/Soybean_2795_Inbred.tar.gz) : Soybean_2795_Inbred

There will be more detailed instructions in the SNPGT Usage below.

## 🌟 Installation
### LinSNPGT requires :
  - **Python3**
  - **bowtie2**
  - **samtools**
  - **[java8](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)**
  - If you want to use **SNPGT-build**, you will also need to install **seqtk**

### Installing
```
git clone https://github.com/Min-Zer0/LinSNPGT.git

cd LinSNPGT
chmod +x ./install.sh && ./install.sh

# install java8
./install.Java8.sh

# install bowtie2
sudo apt install bowtie2

# install samtools
sudo apt install samtools

# install seqtk if you want to use **SNPGT-build**
sudo apt-get install seqtk
```

## 🌟 SNPGT
There are three subfolders and three files after LinSNPGT being installed.

- **.sys**
- **01.Reference_Genome**
- **02.Input_Fastq**
- `SNPGT-build.py`
- `SNPGT.config`
- `SNPGT.py`

To run LinSNPGT via `SNPGT.py`, you need to fill in the `SNPGT.config` and put files in the corresponding path.

Here are the steps:

1. Fill in the `config.txt` file
	- Software Path: Generally, this content does not need to be changed.
 	- Project_Name: Enter your project name which will be output file prefix.	 
	- RefDataSetFile: Enter your dataset corresponding to the model to be fitted.
		- Available species and datasets has been listed above, including their download links.
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
	
	#=================== LinSNPGT Config =======================#
	* [Project]
	Project_Name=Rice
	
	* [Species and Dataset]
	RefDataSet_File=Rice_705_Inbred
	
	* [Running LinSNPGT Thread]
	Thread_Count=10
	
	* [Samples_list]
	> ===========================================
	> |sample | Read1          | Read2          |
	> -------------------------------------------
	  | Line1 | test1_1.fastq.gz | test1_2.fastq.gz |
	  | Line2 | test2_1.fastq.gz | test2_2.fastq.gz |
	
	```
	

2. Download the RefDataSetFile file  `(*.tar.gz)` and move it to the path: **./01.Reference_Genome** 
3. Move your raw sequencing data `(*.fastq.gz)` or `(*.fastq)` to the path: **./02.Input_Fastq**
4. run the command: `python SNPGT.py`

### Output & Analysis
- After the program is completed, the result file will be output in the Result/ directory.
	- ***Standard format VCF (variant call format) file***
	- ****.Genotype.txt***  （Sample genotyping matrix, the format is as follows) 

	CHROM|POS|Line 1|line 2|...|line N|
	---|---|---|---|---|---|
	Chr1|128960|A|.|...|C|
	Chr1|133137|C|C|...|T|
	...|...|...|...|...|...|...|
	Chr12|321216|A|A|...|A|
	Chr12|364257|A|C|...|C|
	Chr12|364755|.|.|...|.|
	...|...|...|...|...|...|...|

- Upload ****.Genotype.txt*** to CropGS-Hub to complete subsequent analysis
	- Phenotype Prediction  **[PhenotypePrediction](https://iagr.genomics.cn/CropGS/#/PhenotypePrediction)** 	
	- Crossing Design  **[CrossingDesign](https://iagr.genomics.cn/CropGS/#/CrossingDesign)**


## 🌟 SNPGT-build
If you are not limited to the dataset of 14 populations provided by our program, you can try to use **SNPGT-build** to make your own RefDataSetFile, and then use SNPGT to complete genotyping.

`python SNPGT-build.py -h`

```
usage: SNPGT-build.py [-h] [-F FASTA] [-B BIM] [-S SPECIES] [-N STRAIN] [-L BINLEN] [--JavaPath JAVAPATH] [--SamtoolsPath SAMTOOLSPATH] [--SeqtkPath SEQTKPATH]
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
`python SNPGT-build.py -F path_to/Rice.fa -B path_to/Rice_378_Inbred.bim -S Rice -N 378_Inbre`

## 👥 Contacts
Jie Qiu (qiujie@shnu.edu.cn)  
Min Zhu (zer0min@outlook.com)  
Jiaxin Chen (jxchen1217@gmail.com)



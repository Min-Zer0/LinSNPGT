#!/usr/bin/python
import os
import time

def Alignment(Reference_dir,Species,Sample,Read1,Read2,Thread):
	os.system('bowtie2 -p %s \
		-x ./01.Reference_Genome/%s/SNP_intervals \
		-U ./02.Input_Fastq/%s ./02.Input_Fastq/%s \
		-S ./temp.sam'%(Thread,Reference_dir,Read1,Read2))
	time.sleep(1)
	os.system('samtools view -h \
		-F 4 ./temp.sam > ./mapped.sam && rm -rf ./temp.sam')
	os.system('samtools fastq -0 \
		./read.fastq ./mapped.sam && rm -rf ./mapped.sam')
	os.system('bowtie2 -p %s \
		-x ./01.Reference_Genome/%s/%s \
		-U ./read.fastq\
		--rg-id %s \
		--rg "PL:ILLUMINA" \
		--rg "SM:%s" \
		-S ./%s.sam'%(Thread,Reference_dir,Species,Sample,Sample,Sample))
	os.system('rm -rf ./read.fastq')
	os.system('samtools view -bS \
		./%s.sam -t ./01.Reference_Genome/%s/%s.fai > ./%s.bam && \
		rm -rf ./%s.sam'%(Sample,Reference_dir,Species,Sample,Sample))
	os.system('samtools sort -@ %s\
		-o ./%s.sorted.bam ./%s.bam && rm -rf ./%s.bam'%(Thread,Sample,Sample,Sample))

def  Merge_rmPCRdup(Project,Thread):
	os.system('mkdir -p ./samplebamfile && mv ./*.sorted.bam ./samplebamfile')
	os.system('samtools merge ./%s.sorted.bam \
		./samplebamfile/*.sorted.bam && rm -rf ./samplebamfile'%(Project))
	os.system('samtools rmdup -sS ./%s.sorted.bam \
		./%s.rmdup.bam && rm -rf ./%s.sorted.bam'%(Project,Project,Project))
	os.system('samtools sort -@ %s -o ./%s.rmdup.sorted.bam \
		./%s.rmdup.bam && rm -rf ./%s.rmdup.bam'%(Thread,Project,Project,Project))
	os.system('samtools index \
		./%s.rmdup.sorted.bam'%(Project))

def Calling_SNP(Reference,ref,Project,Intervals,Thread):
	os.system('./jdk/bin/java -Xmx%sg -jar ./GenomeAnalysisTK.jar \
		-T RealignerTargetCreator \
		-R ./01.Reference_Genome/%s \
		-I ./%s.rmdup.sorted.bam \
		-o ./%s.realn.intervals'%(Thread,Reference,Project,Project))
	os.system('./jdk/bin/java -Xmx%sg -jar ./GenomeAnalysisTK.jar \
		-T IndelRealigner \
		-R ./01.Reference_Genome/%s \
		-targetIntervals ./%s.realn.intervals \
		-I ./%s.rmdup.sorted.bam \
		-o ./%s.realn.bam'%(Thread,Reference,Project,Project,Project))
	os.system('mv ./01.Reference_Genome/%s ./'%(Intervals))
	os.system('./jdk/bin/java -Xmx%sg -jar ./GenomeAnalysisTK.jar \
		-T UnifiedGenotyper \
		--genotype_likelihoods_model SNP\
		-R ./01.Reference_Genome/%s \
    	-I ./%s.realn.bam \
    	-L ./%s.intervals\
    	-o ./%s.raw.vcf \
    	--output_mode EMIT_ALL_SITES'%(Thread,Reference,Project,ref,Project))
	os.system('mv ./%s.intervals ./01.Reference_Genome/%s'%(ref,Intervals))
	os.system('rm -rf ./%s.rmdup.sorted.bam ./%s.rmdup.sorted.bam.bai \
		./%s.realn.bam ./%s.realn.bai ./%s.realn.intervals \
		./%s.raw.vcf.idx'%(Project,Project,Project,Project,Project,Project))

def VCF2Genotyping(Project,SamplesNum):
	sample_col=''
	for i in range(SamplesNum):
		sample_col = sample_col+',$'+str(10+i)
		col_num = "$1,$2,$4,$5"+sample_col
	os.system("grep -v '##' %s.raw.vcf | awk '{print %s}' > %s.vcf2Genotyping.txt"%(Project,col_num,Project))
	VCF_df = open(Project+'.vcf2Genotyping.txt', 'r')
	with open(Project+'.Genotype.txt', 'w') as fw:
		for line in VCF_df:
			if line[0] == "#":
				outputline=line[:-1].split(' ')[0:2] + line[:-1].split(' ')[4:SamplesNum+4]
				fw.write('\t'.join(map(str, outputline)))
				fw.write('\n')
			else:
				info = line[:-1].split(" ")
				ChrNum = info[0]
				Pos = info[1]
				bas = [info[2]] + info[3].split(',')
				outputline=[ChrNum,Pos]
				for i in range(SamplesNum):
					SNP = info[4+i].split(':')[0].split('/')
					if SNP[0] != SNP[1]:
						outputline = outputline + ['H']
					else:
						if SNP[0] == '.':
							outputline = outputline + ['.']
						else:
							outputline = outputline + [bas[int(SNP[0])]]
				fw.write('\t'.join(map(str, outputline)))
				fw.write('\n')
	os.system('rm -rf %s.vcf2Genotyping.txt'%Project)

# Open the config.txt file 
with open('config.txt', 'r') as file:
    lines = file.readlines()
Info_lines = [line.strip() for line in lines if line.strip() and not line.startswith(('>', '#' ,'*'))]

samples_list = []

# Read file 
for line in Info_lines:
	info = line.split('=')
	if info[0] == "Project_Name":
		project = info[1]
	if info[0] == "RefDataSetFile":
		Spec_Ref = info[1]
	elif info[0] == "Thread_Count":
		thread = info[1]
	
	if line[0] == '|':
		sample_info = [item.replace(' ', '') for item in line.split('|')]
		samples_list.append(sample_info[1:-1])

spec_ref = Spec_Ref.split('/')[-1][:-7]
species = spec_ref.split('_')[0]
reference = spec_ref.split('_')[1] + '_' + spec_ref.split('_')[2]

if os.path.exists(r'./01.Reference_Genome/%s.tar.gz' % (spec_ref)) == False and\
	  os.path.exists(r'./01.Reference_Genome/%s' % (spec_ref)) == False:
	print("ERROR: Dataset index does not exist!")
	print("Please ensure that you have moved the downloaded file (*.tar.gz) to the path: ./01.Reference_Genome.")
	os._exit()
else:
	os.system('tar -zxvf ./01.Reference_Genome/%s.tar.gz > /dev/null 2>&1' % (spec_ref))
	os.system('mv %s ./01.Reference_Genome > /dev/null 2>&1' % (spec_ref))
	os.system('rm ./01.Reference_Genome/%s.tar.gz > /dev/null 2>&1' % (spec_ref))
	files = os.listdir(r'01.Reference_Genome/%s'%(species+'_'+reference))
	if {species+'.fasta',species+'.fasta.fai',
		species+'.1.bt2',species+'.2.bt2',species+'.3.bt2',species+'.4.bt2',
		species+'.rev.1.bt2',species+'.rev.2.bt2',species+'.dict',
		reference+'.intervals',
		'SNP_intervals.fasta',
		'SNP_intervals.1.bt2','SNP_intervals.2.bt2','SNP_intervals.3.bt2','SNP_intervals.4.bt2',
		'SNP_intervals.rev.1.bt2','SNP_intervals.rev.2.bt2'} == set(files):
		print("Indexing of the dataset has been completed, go on!")
	else:
		print("Dataset index file corruption! Re-download and move the file.")
		os.system('rm -rf .sys/Reference_Genome/%s > /dev/null 2>&1' % (species + '_' + reference))
		os._exit()

gz_files = os.listdir(r'./02.Input_Fastq/')
if len(gz_files) == 0:
	print("ERROR: Reads file does not exist!")
	print("Please ensure that you have moved the reads file (*.fastq.gz) to the path: ./02.Input_Fastq.")
	os._exit()
else:
	files_nums = len(gz_files)
	for i in range(files_nums):
		os.system('gunzip ./02.Input_Fastq/%s > /dev/null 2>&1' % (gz_files[i]))
		print(gz_files[i]," have been unziped")

	alignment_reference_dir = species + '_' + reference
	gatk_reference = species + '_' + reference + '/' + species + '.fasta'
	intervals = species + '_' + reference + '/' + reference + '.intervals'

	for i in samples_list:
		print(i)
		Alignment(alignment_reference_dir, species, i[0], i[1], i[2], thread)
	Merge_rmPCRdup(project, thread)
	Calling_SNP(gatk_reference, reference, project, intervals, thread)
	VCF2Genotyping(project, len(samples_list))
	print("done!")

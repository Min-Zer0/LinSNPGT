#!/usr/bin/python

import os
import datetime
import subprocess

def check_java(Java_Path):
    try:
        result = subprocess.run([Java_Path, '-version'], capture_output=True, text=True)
        output = result.stderr
        java_version = output.splitlines()[0].split()[2].replace('"', '')
        if java_version.startswith('1.8'):
            return True
        else:
            return False
    except FileNotFoundError:
        return False
    
def check_bowtie2(Bowtie2_Path):
    try:
        subprocess.check_output(["which", Bowtie2_Path])
        return True
    except subprocess.CalledProcessError:
        return False
        
def check_samotools(Samtools_Path):
    try:
        subprocess.check_output(["which", Samtools_Path])
        return True
    except subprocess.CalledProcessError:
        return False

def print_table(data):
	col_width = [max(len(str(x)) for x in col) for col in zip(*data)]
	for row in data:
		row_formatted = " | ".join("{:<{width}}".format(cell, width=col_width[i]) for i, cell in enumerate(row))
	print("=" * len(row_formatted))
	col_width = [max(len(str(x)) for x in col) for col in zip(*data)]
	for row in data:
		row_formatted = " | ".join("{:<{width}}".format(cell, width=col_width[i]) for i, cell in enumerate(row))
		print(row_formatted)
		if row == data[0]:
			print("-" * len(row_formatted))
	print("-" * len(row_formatted))
        
def Alignment(Bowtie2_Path,Samtools_Path,Reference_dir,Species,Sample,Read1,Read2,Thread):
	os.system('%s -p %s \
		-x ./01.Reference_Genome/%s/SNP_intervals \
		-U ./02.Input_Fastq/%s,./02.Input_Fastq/%s \
		-S ./temp.sam'%(Bowtie2_Path,Thread,Reference_dir,Read1,Read2))
	os.system('%s view -h \
		-F 4 ./temp.sam > ./mapped.sam && rm -rf ./temp.sam'%(Samtools_Path))
	os.system('%s fastq -0 \
		./read.fastq ./mapped.sam && rm -rf ./mapped.sam'%(Samtools_Path))
	os.system('%s -p %s \
		-x ./01.Reference_Genome/%s/%s \
		-U ./read.fastq\
		--rg-id %s \
		--rg "PL:ILLUMINA" \
		--rg "SM:%s" \
		-S ./%s.sam'%(Bowtie2_Path,Thread,Reference_dir,Species,Sample,Sample,Sample))
	os.system('rm -rf ./read.fastq')
	os.system('%s view -bS \
		./%s.sam -t ./01.Reference_Genome/%s/%s.fai > ./%s.bam && \
		rm -rf ./%s.sam'%(Samtools_Path,Sample,Reference_dir,Species,Sample,Sample))
	os.system('%s sort -@ %s\
		-o ./%s.sorted.bam ./%s.bam && rm -rf ./%s.bam'%(Samtools_Path,Thread,Sample,Sample,Sample))

def  Merge_rmPCRdup(Samtools_Path,Project,Thread):
	os.system('mkdir -p ./samplebamfile && mv ./*.sorted.bam ./samplebamfile')
	os.system('%s merge ./%s.sorted.bam \
		./samplebamfile/*.sorted.bam && rm -rf ./samplebamfile'%(Samtools_Path,Project))
	os.system('%s rmdup -sS ./%s.sorted.bam \
		./%s.rmdup.bam && rm -rf ./%s.sorted.bam'%(Samtools_Path,Project,Project,Project))
	os.system('%s sort -@ %s -o ./%s.rmdup.sorted.bam \
		./%s.rmdup.bam && rm -rf ./%s.rmdup.bam'%(Samtools_Path,Thread,Project,Project,Project))
	os.system('%s index \
		./%s.rmdup.sorted.bam'%(Samtools_Path,Project))

def Calling_SNP(Java_Path,Reference,ref,Project,Intervals,Thread):
	os.system('%s -Xmx%sg -jar .sys/GenomeAnalysisTK.jar \
		-T RealignerTargetCreator \
		-R ./01.Reference_Genome/%s \
		-I ./%s.rmdup.sorted.bam \
		-o ./%s.realn.intervals'%(Java_Path,Thread,Reference,Project,Project))
	os.system('%s -Xmx%sg -jar .sys/GenomeAnalysisTK.jar \
		-T IndelRealigner \
		-R ./01.Reference_Genome/%s \
		-targetIntervals ./%s.realn.intervals \
		-I ./%s.rmdup.sorted.bam \
		-o ./%s.realn.bam'%(Java_Path,Thread,Reference,Project,Project,Project))
	os.system('mv ./01.Reference_Genome/%s ./'%(Intervals))
	os.system('%s -Xmx%sg -jar .sys/GenomeAnalysisTK.jar \
		-T UnifiedGenotyper \
		--genotype_likelihoods_model SNP\
		-R ./01.Reference_Genome/%s \
    	-I ./%s.realn.bam \
    	-L ./%s.intervals\
    	-o ./%s.raw.vcf \
    	--output_mode EMIT_ALL_SITES'%(Java_Path,Thread,Reference,Project,ref,Project))
	os.system('mv ./%s.intervals ./01.Reference_Genome/%s'%(ref,Intervals))
	os.system('rm -rf ./%s.rmdup.sorted.bam ./%s.rmdup.sorted.bam.bai \
		./%s.realn.bam ./%s.realn.bai ./%s.realn.intervals \
		./%s.raw.vcf.idx'%(Project,Project,Project,Project,Project,Project))

def VCF2Genotyping(Project,SamplesNum,Reference):
	sample_col=''
	for i in range(SamplesNum):
		sample_col = sample_col+',$'+str(10+i)
		col_num = "$1,$2,$4,$5"+sample_col
	os.system("grep -v '##' %s.raw.vcf | awk '{print %s}' > %s.vcf2Genotyping.txt"%(Project,col_num,Project))
	VCF_df = open(Project+'.vcf2Genotyping.txt', 'r')
	formatted_datetime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	with open(Project+'.Genotype.txt', 'w') as fw:
		fw.write('##Date=%s\n'%formatted_datetime)
		fw.write('##Reference=%s\n'%Reference)
		fw.write('##Project=%s\n'%Project)
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
	current_date = datetime.date.today()
	folder_name = str(current_date)+"_result"
	os.system('mkdir -p %s && mv %s.Genotype.txt %s.raw.vcf %s'%(folder_name,Project,Project,folder_name))

# Open the config.txt file 
with open('SNPGT.config', 'r') as file:
    lines = file.readlines()
Info_lines = [line.strip() for line in lines if line.strip() and not line.startswith(('>', '#' ,'*'))]

samples_list = []

# Read file 
for line in Info_lines:
	info = line.split('=')
	if info[0] == "Java_Path":
		Java_Path = info[1]
	if info[0] == "Bowtie2_Path":
		Bowtie2_Path = info[1]
	if info[0] == "Samtools_Path":
		Samtools_Path = info[1]	
	if info[0] == "Project_Name":
		project = info[1]
	if info[0] == "RefDataSet_File":
		Spec_Ref = info[1]
		if not Spec_Ref.endswith('.tar.gz'):
			Spec_Ref += '.tar.gz'
	elif info[0] == "Thread_Count":
		thread = info[1]
	if line[0] == '|':
		sample_info = [item.replace(' ', '') for item in line.split('|')]
		samples_list.append(sample_info[1:-1])

spec_ref = Spec_Ref[:-7]
species = spec_ref.split('_')[0]
reference = spec_ref.split('_')[1] + '_' + spec_ref.split('_')[2]

print(40*"*")
print("Checking software configuration")

print(">>> java")
if check_java(Java_Path):
    print("Done !\n")
else:
    print("Java8 is not installed.\n")
    os._exit()
    
print(">>> bowtie2")
if check_bowtie2(Bowtie2_Path):
    print("Done !\n")
else:
    print("bowtie2 is not installed.\n")
    os._exit()

print(">>> samtools")
if check_samotools(Samtools_Path):
    print("Done !\n")
else:
    print("samtools is not installed.\n")
    os._exit()
print(40*"*")

print(">>> Project\n",project,"\n")
print(">>> Species and Dataset\n",species,"\n",reference,"\n")
print(">>> Samples_list")
print_table([["sample","Read1","Read2"]] + samples_list)
input("\nPress Enter to confirm and continue ...")


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
		os.system('rm -rf ./01.Reference_Genome/%s > /dev/null 2>&1' % (species + '_' + reference))
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
		for x in range(2):
			if i[x+1].endswith('.gz'):
				i[x+1] = i[x+1][:-3]
		print("\n")
		print_table([i])
		Alignment(Bowtie2_Path,Samtools_Path,alignment_reference_dir, species, i[0], i[1], i[2], thread)
	Merge_rmPCRdup(Samtools_Path,project, thread)
	Calling_SNP(Java_Path,gatk_reference, reference, project, intervals, thread)
	VCF2Genotyping(project, len(samples_list),reference)
	print("done!")

#!/usr/bin/python

import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description='SNPGT-build (Tools for make RefGenome)')
parser.add_argument('-F', '--fasta', help='Whole genome reference sequence')
parser.add_argument('-B', '--bim', help='SNP site information(bim file)')
parser.add_argument('-S', '--species', help='Specify species name; eg. Rice')
parser.add_argument('-N', '--strain', help='Specify strain name; eg. 378_Inbred')
parser.add_argument('-L', '--binlen',default=400, type=int, help='The simplified of the genome retains base length on both sides of the SNP. The default value is 400')
parser.add_argument('--JavaPath',default="./jdk/bin/java", type=str, help='Path to java8. The default is ./jdk/bin/java')
parser.add_argument('--SamtoolsPath',default="samtools", type=str, help='Path to samtools.')
parser.add_argument('--SeqtkPath',default="seqtk", type=str, help='Path to Seqtk.')
parser.add_argument('--Bowtie2Path',default="bowtie2-build", type=str, help='Path to bowtie2-build.')
args = parser.parse_args()\

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
    
def check_samotools(Samtools_Path):
    try:
        subprocess.check_output(["which", Samtools_Path])
        return True
    except subprocess.CalledProcessError:
        return False
def check_seqtk(Seqtk_Path):
    try:
        subprocess.check_output(["which", Seqtk_Path])
        return True
    except subprocess.CalledProcessError:
        return False
def check_bowtie2(Bowtie2_Path):
    try:
        subprocess.check_output(["which", Bowtie2_Path])
        return True
    except subprocess.CalledProcessError:
        return False

def Checking_software():
	print(40*"*")
	print("Checking software configuration")

	print(">>> java")
	if check_java(Java_Path):
		print("Done ！\n")
	else:
		print("Java8 is not installed.\n")
		os._exit()

	print(">>> bowtie2-build")
	if check_bowtie2(Bowtie2_build):
		print("Done ！\n")
	else:
		print("bowtie2 is not installed.\n")
		os._exit()
    
	print(">>> samtools")
	if check_samotools(Samtools_Path):
		print("Done ！\n")
	else:
		print("samtools is not installed.\n")
		os._exit()

	print(">>> seqtk")
	if check_seqtk(Seqtk_Path):
		print("Done ！\n")
	else:
		print("seqtk is not installed.\n")
		os._exit()
			
	print(40*"*")

def SplitRef(Ref_file, Chr_list,Samtools_Path):
    os.system("mkdir ./Chr_fa")
    for ChrNum in Chr_list:
        os.system("%s faidx %s %s > ./Chr_fa/%s.fasta" % (Samtools_Path, Ref_file, ChrNum, ChrNum))
        os.system("awk '{print $1,$2}' %s.fai > ./lengths.txt" % (Ref_file))

def Find_SNP_Section(Chr_intervals, Section_len_half, Chr_len):
    SNP_section = []
    for SNP_pos in Chr_intervals:
        if SNP_pos < Section_len_half:
            section = [0, SNP_pos + Section_len_half]
            SNP_section.append(section)
        elif SNP_pos + Section_len_half > Chr_len:
            section = [SNP_pos - Section_len_half, Chr_len]
            SNP_section.append(section)
        else:
            section = [SNP_pos - Section_len_half, SNP_pos + Section_len_half]
            SNP_section.append(section)
    return SNP_section

def merge_ranges(ranges):
    sorted_ranges = sorted(ranges)
    merged_ranges = []
    for start, end in sorted_ranges:
        if merged_ranges and start <= merged_ranges[-1][1]:
            merged_ranges[-1] = (merged_ranges[-1][0], max(end, merged_ranges[-1][1]))
        else:
            merged_ranges.append((start, end))
    return merged_ranges

def MakeREF(fasta, bim ,spec_line,Java_Path,Bowtie2_build,Samtools_Path,Seqtk_Path):
	os.system("awk '{position=$1\":\"$4\"-\"$4;print position}' \
			%s > %s.intervals" %(bim,spec_line[1]))
	os.system("mv %s %s" %(fasta, spec_line[0]+".fasta"))
	Ref_file = spec_line[0]+".fasta"
	intervals_file = "%s.intervals" %(spec_line[1])

	os.system("%s faidx %s" % (Samtools_Path, Ref_file))
	os.system("%s -jar .sys/picard.jar CreateSequenceDictionary R=%s" % (Java_Path,Ref_file))

	Chr_list = []
	intervals_df = open(intervals_file, 'r')
	for line in intervals_df:
		ChrNum = line[:-1].split(":")[0]
		if ChrNum not in Chr_list:
			Chr_list.append(ChrNum)
	intervals_df.close()

	SplitRef(Ref_file, Chr_list, Samtools_Path)

	fw = open("./SNP_intervals.bed",'w')
	for ChrNum in Chr_list:
		Chr_len = ''
		for line in open("./lengths.txt", "r"):
			if line.split(" ")[0] == ChrNum:
				Chr_len = int(line[:-1].split(" ")[1])
		Chr_intervals = []
		for line in open(intervals_file, 'r'):
			if line[:-1].split(":")[0] == ChrNum:
				Chr_intervals.append(int(line[:-1].split(":")[1].split("-")[0]))
		SNP_section = Find_SNP_Section(Chr_intervals, Section_len_half, Chr_len)
		SNP_meraged_section =  merge_ranges(SNP_section)
		for SNP_section in SNP_meraged_section:
			fw.write(str(ChrNum)+"\t")
			fw.write(str(SNP_section[0])+"\t")
			fw.write(str(SNP_section[1])+"\n")
	fw.close()

	os.system("%s subseq %s SNP_intervals.bed > SNP_intervals.fasta"%(Seqtk_Path,Ref_file))
	os.system("rm -rf lengths.txt SNP_intervals.bed Chr_fa/ ")

	result_file = spec_line[0]+"_"+spec_line[1]
	os.system("mkdir %s" %(result_file))
	os.system("mv %s.fasta %s.fasta.fai %s.dict %s.intervals SNP_intervals.fasta %s" 
		%(spec_line[0],spec_line[0],spec_line[0],spec_line[1],result_file))

	os.system("%s %s/%s.fasta %s/%s"
		%(Bowtie2_build,result_file,spec_line[0],result_file,spec_line[0]))
	os.system("%s %s/SNP_intervals.fasta %s/SNP_intervals"
		%(Bowtie2_build,result_file,result_file))        
	os.system("mv %s ./01.Reference_Genome/"%(result_file))


Java_Path = args.JavaPath
Bowtie2_build = args.Bowtie2Path
Samtools_Path = args.SamtoolsPath
Seqtk_Path = args.SeqtkPath
Checking_software()
input("\nPress Enter to confirm and continue ...")
fasta = args.fasta
bim = args.bim
spec = args.species
line_type = args.strain
spec_line = [spec,line_type]
Section_len_half = args.binlen/2

MakeREF(fasta, bim ,spec_line,Java_Path,Bowtie2_build,Samtools_Path,Seqtk_Path)

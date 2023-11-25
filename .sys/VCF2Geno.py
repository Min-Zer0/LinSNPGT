import os

def VCF2Genotyping(VCF_file,Geno_type):
    VCF_df = open(VCF_file, 'r')
    with open(Geno_type, 'w') as fw:
        for line in VCF_df:
            if line[:2] != "##":
                if line[0] == "#":
                    SamplesNum = len(line.strip().split("\t"))
                    line_list = line.strip().split("\t")
                    outputline = line_list[0:2]  + line_list[9:SamplesNum]
                    fw.write('\t'.join(map(str, outputline)))
                    fw.write('\n')
                else:
                    info = line.strip().split("\t")
                    ChrNum = info[0]
                    Pos = info[1]
                    bas = [info[3]] + info[4].split(',')
                    outputline = [ChrNum, Pos]
                    for i in range(SamplesNum-9):
                        SNP = info[9 + i].split(':')[0].split('/')
                        if SNP[0] != SNP[1]:
                            outputline = outputline + ['H']
                        else:
                            if SNP[0] == '.':
                                outputline = outputline + ['.']
                            else:
                                outputline = outputline + [bas[int(SNP[0])]]
                    fw.write('\t'.join(map(str, outputline)))
                    fw.write('\n')

current_directory = os.getcwd()
all_files = os.listdir(current_directory)
vcf_files = [file for file in all_files if file.endswith('.vcf')]

for input_file_path in vcf_files:
    print("In the process of handling " + input_file_path + "...")
    output_file_path = input_file_path.split(".vcf")[0]+"Training.geno"
    VCF2Genotyping(input_file_path,output_file_path)
    print("Done!")

input("Press any key to exit.")
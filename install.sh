#!/bin/bash

mkdir 01.Reference_Genome 02.Input_Fastq
mv .sys/install.Java8.sh .sys/SNPGT-build.py .sys/SNPGT.py .sys/SNPGT.config ./
chmod +x install.Java8.sh SNPGT-build.py SNPGT.py
chmod +x .sys/picard.jar .sys/GenomeAnalysisTK.jar
mv install.sh .sys/
echo "----------------------------"
echo "|  Install has completed ! |"
echo "----------------------------"

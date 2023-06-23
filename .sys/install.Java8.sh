#!/bin/bash

wget --no-cookies --no-check-certificate \
    --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" \
    "http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz"
tar -zxvf ./jdk-8u141-linux-x64.tar.gz
mv jdk1.8.0_141 jdk
rm ./jdk-8u141-linux-x64.tar.gz
echo "=========================================="
./jdk/bin/java -version
echo "=========================================="
echo "Java8 has been installed !"
mv ./install.Java8.sh .sys

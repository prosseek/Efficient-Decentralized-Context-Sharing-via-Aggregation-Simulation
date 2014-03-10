#!/bin/sh
JYTHON="java -jar /Users/smcho/Dropbox/smcho/bin/jar/jython/jython-standalone-2.7-b1.jar"
PACKAGE_NAME=$(basename "$PWD")
args=`getopt tj`

JYTHON_TEST=0
TIME=0

# parameter setup
for i 
do
    if [ $i == "-t" ];
    then
        TIME=1
    fi
    if [ $i == "-j" ];
    then
        JYTHON_TEST=1
    fi
done

result=$(ls $PACKAGE_NAME/*.py)

for i in $result
do
    if [ "$i" == "$PACKAGE_NAME/__init__.py" ];
    then
        continue
    fi
    
    echo "PYTHON TEST running ... $i"
    if [ $TIME -eq 1 ];
    then
        time python $i
    else
        python $i
    fi
    
    if [ $JYTHON_TEST -eq 1 ];
    then
        echo "JYTHON TEST running ... $i"
        
        if [ $TIME -eq 1 ];
        then
            time $JYTHON $i
        else
            $JYTHON $i
        fi  
    fi
done
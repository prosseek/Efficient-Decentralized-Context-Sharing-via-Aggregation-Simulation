#!/bin/sh
PTHS=../context:../context_aggregator:.
PYTHON_PATH="export PYTHONPATH=$PTHS"
JYTHON_PATH="export JYTHONPATH=$PTHS"
JYTHON="$JYTHON_PATH; java -jar /Users/smcho/Dropbox/smcho/bin/jar/jython/jython-standalone-2.7-b1.jar"
PACKAGE_NAME=$(basename "$PWD")
args=`getopt tj`

JYTHON_TEST=0
TIME=0

PYTON_EXECUTABLE="/usr/bin/python"
PYH="$PYTHON_PATH; $PYTON_EXECUTABLE"

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
        time eval $PYH $i
    else
        #echo $PYH
        #echo $i
        eval $PYH $i
    fi
    
    if [ $JYTHON_TEST -eq 1 ];
    then
        echo "JYTHON TEST running ... $i"
        
        if [ $TIME -eq 1 ];
        then
            time eval $JYTHON $i
        else
            eval $JYTHON $i
        fi  
    fi
done
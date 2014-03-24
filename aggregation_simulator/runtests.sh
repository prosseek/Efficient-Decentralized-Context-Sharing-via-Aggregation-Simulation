#!/bin/sh
PTHS=../context:../context_aggregator:.
PYTHON_PATH="export PYTHONPATH=$PTHS"
JYTHON_PATH="export JYTHONPATH=$PTHS"
JYTHON_JAR="java -jar /Users/smcho/Dropbox/smcho/bin/jar/jython/jython-standalone-2.7-b1.jar"
JYTHON="$JYTHON_PATH; $JYTHON_JAR"
PACKAGE_NAME=$(basename "$PWD")
args=`getopt tj`

JYTHON_TEST=0
TIME=0

PTH="context_aggregator/dataflow.py"
PYTON_EXECUTABLE="/usr/bin/python"
PYH="$PYTHON_PATH; $PYTON_EXECUTABLE"

SKIPLIST="simulator.py __init__.py"

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
    skipit=0
    for skip in $SKIPLIST;
    do
        #echo $skip
        if [ "$i" == "$PACKAGE_NAME/$skip" ];
        then
            skipit=1
            break
        fi
    done
    
    if [ $skipit == 1 ];
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
            echo $JYTHON $i
            eval $JYTHON $i
        fi  
    fi
done

python rununittests.py

if [ $JYTHON_TEST -eq 1 ];
then
    echo "JYTHON UNITTEST running ... $i"
    $JYTHON_JAR rununittests.py
fi

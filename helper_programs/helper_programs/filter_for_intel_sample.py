"""From source data (data.txt) to filtering to get smaller set of data data_small.txt

1. It is for intel data
2. Use this to generate another set of sample data
"""

id_set = set()
        
with open("data.txt","r") as f:
    global buf
    buf = ""
    while True:
        read = f.readline()
        if not read: break

        date, time, epoch, id_node, temp, humid, light, voltage = read.split(' ')
        hour, minute, sec = time.split(':')
        if date == '2004-02-28' and hour == '15' and minute in ['08','09','10','11','12','13','14']:
            buf += read
            id_set.add(int(id_node))

    f.close()

maxi = max(id_set)
mini = min(id_set)
full_value = set([i for i in range(mini, maxi+1)])
print full_value - id_set
    
with open("data_small2.txt","w") as f:
    f.write(buf)
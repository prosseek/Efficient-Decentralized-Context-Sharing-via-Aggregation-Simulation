"""From small data to sample generator

1. this is for intel data simulation
"""
buf_dict = {}
        
with open("data_small2.txt","r") as f:
    global buf
    buf = ""
    while True:
        read = f.readline()
        if not read: break

        date, time, epoch, id_node, temp, humid, light, voltage = read.split(' ')
        hour, minute, sec = time.split(':')
        
        id_node = int(id_node)
        if id_node not in buf_dict:
            buf_dict[id_node] = []
        buf_dict[id_node].append(read)    
    f.close()

f = open("sample.txt","w")

for i in sorted(buf_dict):
    read = buf_dict[i]
    read = read[0]
    date, time, epoch, id_node, temp, humid, light, voltage = read.split(' ')
    f.write("%s: %s\n" % (id_node, temp))
f.close()
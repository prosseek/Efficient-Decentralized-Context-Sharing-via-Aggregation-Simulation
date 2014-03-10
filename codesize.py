from subprocess import *
import os
import re

class CodeSize(object):
    """
    Find the total code size in directory
    """
    def __init__(self):
        self.dictionary = {}

    ## 1st possibility
    def getFiles(self, directory, fileExtension, skip = None):
        def getAllFiles(directory, extension = None, skip = None):
            result = []
            if skip is None: skip = []

            # dirname is current directory, and dirnames/filenames are the contents in the directory
            # os.walk seems to be a generator to yield all the directory names until none left
            for dirname, dirnames, filenames in os.walk(directory): 

                for filename in filenames:
                    pathName = os.path.join(dirname, filename)
                    if extension is None:
                        result.append(pathName)
                    elif filename.endswith(extension) and filename not in skip: 
                        result.append(pathName)
            return result
            
        files = getAllFiles(directory, fileExtension, skip)
        for file in files:
            p1 = Popen(["wc", file], stdin=PIPE, stdout=PIPE)
            output = p1.communicate()[0]
            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            #result = output.split('\n')
            r = filter(lambda m: m != '', output.rstrip().split(' '))
            #print r
            self.dictionary[r[-1]] = [r[0], r[1], r[2]]
        
        return self
    
    ## 2nd possibility
    def getFiles2(self, directory, fileExtension, skip=None):
        p1 = Popen(['find', directory, '-name', "*.%s" % fileExtension, "-print"], stdout=PIPE)
        p2 = Popen(["xargs", "wc"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output = p2.communicate()[0]
        #print output
        results = output.split('\n')
        #['      15      22     246 ./test/testUtil.py', 
        # '      15      22     246 ./test/testUtilcopy.py', 
        # '      30      44     492 total', '']
        self.dictionary = {}
        
        for result in results:
            r = filter(lambda m: m != '', result.rstrip().split(' '))
            # ['15', '22', '246', './test/testUtil.py']
            # ['15', '22', '246', './test/testUtilcopy.py']
            # ['30', '44', '492', 'total']
            # []
            if r and r[-1].endswith('py'):
                self.dictionary[r[-1]] = [r[0], r[1], r[2]]
                
        return self

    def __add__(self, other):
        for i,v in other.dictionary.items():
            self.dictionary[i] = v
        return self

    def __str__(self):
        #return str(self.dictionary)
        result = ""
        sum = 0
        
        sortedKeys = sorted(self.dictionary.keys())
        #print sortedKeys
        
        srcSum = 0
        testSum = 0
        
        rex = re.compile("/test/test")
        
        for i in sortedKeys:
        #for i,v in self.dictionary.items():
            v = self.dictionary[i]
            result += i + ":" + v[0] + "\n"
            sum += int(v[0])
            if rex.search(i): 
                testSum += int(v[0])
            else: 
                srcSum += int(v[0])
                
        result += "\nTOTAL: %d \nSRC: %d TEST: %d \nRATIO: %f" % (sum, srcSum, testSum, float(testSum)/float(srcSum))
        return result

if __name__ == "__main__":
    # c = CodeSize()
    # print c.getFiles("./test", "py")
    # 
    d = CodeSize()
    # print d.getFiles("./src", "py")
    # 
    # print c + d
    
    print d.getFiles(".", "py",['codesize.py', 'setup.py', 'testAll.py', 'conf.py', 'compile.py'])

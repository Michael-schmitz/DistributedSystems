import os
import sys
import re
import unittest
class TestSeq(unittest.TestCase):
    def test_seq(self):
        location = '.'
        for filename in os.listdir(location):
            if filename == 'outputSeqMain.log':
                f = open(os.path.join(location,'outputSeqMain.log' ), "r")
                output = f.read()
                f.close()

        #split = output.split("PID:")
        #split2 = "INFO:root:PID:LYTK, Time:7 SET a -> b'5'"

        String2 = []
        String2.append(output)
        pattern = "PID:(.*?)," #Pattern to look for in the 
        substring2 = re.search(pattern,output).group(1) #this will get the PID and compare it with the time to make sure it is in order

        pattern2 = "Time:(.*?)\n" #gets the time to compare that it is in order as well from the output log.
        substring3 = re.search(pattern2,output).group(1)

        def listToString(s): 
            # initialize an empty string
            str1 = "" 
            # traverse in the string  
            for ele in s: 
                str1 += ele  
            # return string  
            return str1 

        dict = {}
        for i in range(1,10): #iterate amount of numbers 
            if substring2 not in dict:
                dict[substring2] = 1
                (self.assertEqual(i,dict.get(substring2), "False")) #compares the id to the time and adds it to a dictionary
            else:
                dict[substring2] += 1
                (self.assertEqual(i,dict.get(substring2), "False")) #continues comparisons if PID is already in the dict
        print("Passed all Tests")

if __name__ == '__main__':
    unittest.main()
#print(output)

#print(listToString(output))    

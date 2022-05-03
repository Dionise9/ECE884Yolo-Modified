# import required module
import os

# assign directory
directory = "C:/lib/DarknetFiles/data/Udacity/export"

location = "data/Udacity/export/"

previous = []

# iterate over files in
# that directory

writer1 = open("C:/lib/Darknet/data/Udacity/train.txt","w")
writer2 = open("C:/lib/Darknet/data/Udacity/valid.txt","w")
writer3 = open("C:/lib/Darknet/data/Udacity/test.txt","w")

noTxtCt = 0

totalCount = 0

valid = 12000
test = 13550

for filename in os.listdir(directory):
    spl = filename.split(".")
    last = spl[-1]
    first = spl[0].split("_")[0]
    if "jpg" == last:
        if first not in previous:
            previous.append(first)
            if not os.path.exists(directory+"/"+filename[:-3]+"txt"):
                mod = noTxtCt%10
                if mod >= 8:
                    writer3.write(location+filename+"\n")
                elif mod >= 6:
                    writer2.write(location + filename + "\n")
                else:
                    writer1.write(location + filename + "\n")
                noTxtCt += 1
            else:
                if totalCount > test:
                    writer3.write(location+filename+"\n")
                elif totalCount > valid:
                    writer2.write(location + filename + "\n")
                else:
                    writer1.write(location + filename + "\n")
            totalCount += 1
        else:
            os.remove(directory+"/"+filename)

print(totalCount)
print(noTxtCt)
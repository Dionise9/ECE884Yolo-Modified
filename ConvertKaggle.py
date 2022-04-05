import csv

file = open("./data/dataset/Kaggle/labels_val.csv")

reader = csv.reader(file)
writer = open("./data/dataset/Kaggle/trainval.txt", "w")

_ = reader.__next__()
first = reader.__next__()
location = "./data/dataset/Kaggle/images"
last = first[0].strip()
s = location+"/"+last+" "+first[1]+","+first[3]+","+first[2]+","+first[4]+","+str(int(first[5])-1)

for line in reader:
    if line[0] == last:
        s += " "+line[1]+","+line[3]+","+line[2]+","+line[4]+","+str(int(line[5])-1)
    else:
        last = line[0]
        writer.write(s)
        writer.write("\n")
        s = location+"/"+last+" "+line[1]+","+line[3]+","+line[2]+","+line[4]+","+str(int(line[5])-1)

writer.write(s)
writer.write("\n")
writer.close()

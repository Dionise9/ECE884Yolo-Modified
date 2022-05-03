import csv

file = open("./data/dataset/Kaggle/labels_trainval.csv")

reader = csv.reader(file)

imgSize = (300, 480)

def BndBox2YoloLine(line):
    xmin = float(line[1])
    xmax = float(line[2])
    ymin = float(line[3])
    ymax = float(line[4])

    xcen = float((xmin + xmax)) / 2 / imgSize[1]
    ycen = float((ymin + ymax)) / 2 / imgSize[0]

    w = float((xmax - xmin)) / imgSize[1]
    h = float((ymax - ymin)) / imgSize[0]

    classIndex = str(int(line[5])-1)

    return classIndex, xcen, ycen, w, h

_ = reader.__next__()
first = reader.__next__()
location = "data/Kaggle/images/"
last = first[0]
fName = last.split(".")[0]
cl,xc,yc,w,h = BndBox2YoloLine(first)
s = str(cl) + " " + str(xc) + " " + str(yc) + " " + str(w) + " " + str(h) + "\n"
writer = open("C:/lib/DarknetFiles/data/Kaggle/images/"+fName+".txt", "w")
writer2 = open("./data/dataset/Kaggle/test.txt", "w")
writer.write(s)
writer2.write(location+last + "\n")

for line in reader:
    if line[0] == last:
        cl, xc, yc, w, h = BndBox2YoloLine(line)
        s = str(cl) + " " + str(xc) + " " + str(yc) + " " + str(w) + " " + str(h) + "\n"
        writer.write(s)
    else:
        writer.close()
        last = line[0]
        writer2.write(location+last + "\n")
        fName = last.split(".")[0]
        writer = open("C:/lib/DarknetFiles/data/Kaggle/images/" + fName + ".txt", "w")
        writer.write(s)
        cl, xc, yc, w, h = BndBox2YoloLine(line)
        s = str(cl) + " " + str(xc) + " " + str(yc) + " " + str(w) + " " + str(h) + "\n"
        writer.write(s)

writer.close()
writer2.close()

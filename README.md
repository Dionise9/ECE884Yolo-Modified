# ECE884Yolo-Modified

This project is divided into two parts, a darknet configuration section and a python/tensorflow code section.

## Introduction

Autonomous Vehicles with Computer Vision are great examples of Cyber- Physical Systems which depend on time-sensitive data recorded from their surrounding environment, in which real-time object detection can be crucial for decision making. 
Effectively, our proposed project was to detect objects in nearby environments accurately without performance delays. With the addition of:
Obtaining a smaller model which is capable enough to be used in embedded systems
Detecting objects of different sizes and/or distances from AV
There are many tradeoffs and factors which can affect Accuracy and Performance (FPS/Processing time).


## Python Tensorflow Implementation

Running training from scratch:
1. Convert dataset CSV to TXT of form location,xmin,ymin,xman,ymax,class
(For AV dataset use ConvertKaggleTensorflow.py)
2. Setup core/config.py, make sure classes point to the class names for the dataset,
make sure train.annot_path and test.annot_path exist
3. Run train.py

When running from checkpoints:
Run train.py --weights ./checkpoints/*model name*

To detect:

```bash
detect.py --weights ./checkpoints/yolov4-416 --image ./Examples/IMG_2878.PNG
```

For using the other methods and functions see [this](https://github.com/hunglc007/tensorflow-yolov4-tflite) repo.

## Darknet Implementation

The bulk of this project used the [AlexyAB darknet](https://github.com/AlexeyAB/darknet) repo.

In order to run the configuration files all that is needed is to build darknet as linked in the above repo.
The configuration files for the tiny and tinier model are included in this repo in the DarknetFiles folder, as well as 
their respective dataset configuration files. The weights are too large for this repo, so in order to get them please
email dionise9@msu.edu.

To detect a video using tinier:

```bash
./darknet detector demo cfg/av.data cfg/yolov4-tinier-av.cfg [yolov4 tinier weights path] [video path]
```

To train the tinier model on the kaggle dataset:

```bash
./darknet detector train cfg/av.data cfg/yolov4-tinier-av.cfg
```
Note that the kaggle dataset needs to be [downloaded](https://www.kaggle.com/datasets/alincijov/self-driving-cars?resource=download) and converted to the darknet form, using ConvertKaggle.py.

## Model and Results

Yolov4-tiny model:
![Yolov4-tiny](https://github.com/Dionise9/ECE884Yolo-Modified/blob/master/DiagramFiles/yolov4-tiny-1.jpg?raw=true)

Our yoloV4-tinier model:
![Yolov4-tinier](https://github.com/Dionise9/ECE884Yolo-Modified/blob/master/DiagramFiles/yolov4-tinier-1.jpg?raw=true)

For the udacity dataset:

Model | mAP | BFLOPs 
--- | --- | ---
Yolo V4 | 32% | 59.636
Yolo V4 Tiny | 16% | 6.803
Yolo V4 Tinier | 15% | 3.561

## Figure Generation

This uses the [PlotNeuralNet](https://github.com/HarisIqbal88/PlotNeuralNet) repo. 
The code is available in the DiagramFiles folder. Follow the repo to see how to install and run PlotNeuralNet.

##License
[MIT](https://choosealicense.com/licenses/mit/)


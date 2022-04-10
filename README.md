# ECE884Yolo-Modified

Running training from scratch:
1. Convert dataset CSV to TXT of form location,xmin,ymin,xman,ymax,class
(For AV dataset use ConvertKaggle.py)
2. Setup core/config.py, make sure classes point to the class names for the dataset,
make sure train.annot_path and test.annot_path exist
3. Run train.py

When running from checkpoints:
Run train.py --weights ./checkpoints/*model name*

To detect:
Run detect.py --weights ./checkpoints/yolov4-416 --image ./Examples/IMG_2878.PNG
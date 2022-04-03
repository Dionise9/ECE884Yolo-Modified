import tensorflow as tf

from tf2_yolov4.anchors import YOLOV4_ANCHORS
from tf2_yolov4.model import YOLOv4

HEIGHT, WIDTH = (640, 960)

model = YOLOv4(
    (HEIGHT, WIDTH, 3),
    80,
    YOLOV4_ANCHORS,
    weights="darknet",
)

image = tf.io.read_file("./Examples/IMG_2878.PNG")
image = tf.image.decode_image(image)
image = tf.image.resize(image, (HEIGHT, WIDTH))
images = tf.expand_dims(image, axis=0) / 255.0



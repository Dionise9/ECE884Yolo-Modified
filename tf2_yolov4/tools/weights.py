"""
Module related to download of original Darknet weights (Keras-style)
"""
from pathlib import Path

import numpy as np

from tf2_yolov4.tools.download import download_file_from_google_drive


TF2_YOLOV4_DEFAULT_PATH = Path.home() / ".tf2-yolov4"
DARKNET_WEIGHTS_PATH = TF2_YOLOV4_DEFAULT_PATH / "yolov4.h5"
DARKNET_ORIGINAL_WEIGHTS_PATH = TF2_YOLOV4_DEFAULT_PATH / "yolov4.weights"

YOLOV4_DARKNET_FILE_ID = "1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT"
YOLOV4_DARKNET_FILE_SIZE = 249 * 1024 * 1024

AVAILABLE_PRETRAINED_WEIGHTS_OPTIONS = ["darknet"]


def load_darknet_weights_in_yolo(yolo_model, darknet_weights_path):
    """
    Load the yolov4.weights file into our YOLOv4 model.

    Args:
        yolo_model (tf.keras.Model): YOLOv4 model
        darknet_weights_path (str): Path to the yolov4.weights darknet file

    Returns:
        tf.keras.Model: YOLOv4 model with Darknet weights loaded.
    """
    model_layers = (
        yolo_model.get_layer("CSPDarknet53").layers
        + yolo_model.get_layer("YOLOv4_neck").layers
        + yolo_model.get_layer("YOLOv3_head").layers
    )

    # Get all trainable layers: convolutions and batch normalization
    conv_layers = [layer for layer in model_layers if "conv2d" in layer.name]
    batch_norm_layers = [
        layer for layer in model_layers if "batch_normalization" in layer.name
    ]

    # Sort them by order of appearance.
    # The first apparition does not have an index, hence the [[0]] trick to avoid an error
    conv_layers = [conv_layers[0]] + sorted(
        conv_layers[1:], key=lambda x: int(x.name[7:])
    )
    batch_norm_layers = [batch_norm_layers[0]] + sorted(
        batch_norm_layers[1:], key=lambda x: int(x.name[20:])
    )

    # Open darknet file and read headers
    darknet_weight_file = open(darknet_weights_path, "rb")
    # First elements of file are major, minor, revision, seen, _
    _ = np.fromfile(darknet_weight_file, dtype=np.int32, count=5)

    # Keep an index of which batch norm should be considered.
    # If batch norm is used with a convolution (meaning conv has no bias), the index is incremented
    # Otherwise (conv has a bias), index is kept still.
    current_matching_batch_norm_index = 0

    for layer in conv_layers:
        kernel_size = layer.kernel_size
        input_filters = layer.input_shape[-1]
        filters = layer.filters
        use_bias = layer.bias is not None

        if use_bias:
            # Read bias weight
            conv_bias = np.fromfile(
                darknet_weight_file, dtype=np.float32, count=filters
            )
        else:
            # Read batch norm
            # Reorder from darknet (beta, gamma, mean, var) to TF (gamma, beta, mean, var)
            batch_norm_weights = np.fromfile(
                darknet_weight_file, dtype=np.float32, count=4 * filters
            ).reshape((4, filters))[[1, 0, 2, 3]]

        # Read kernel weights
        # Reorder from darknet (filters, input_filters, kernel_size[0], kernel_size[1]) to
        # TF (kernel_size[0], kernel_size[1], input_filters, filters)
        conv_size = kernel_size[0] * kernel_size[1] * input_filters * filters
        conv_weights = (
            np.fromfile(darknet_weight_file, dtype=np.float32, count=conv_size)
            .reshape((filters, input_filters, kernel_size[0], kernel_size[1]))
            .transpose([2, 3, 1, 0])
        )

        if use_bias:
            # load conv weights and bias, increase batch_norm offset
            layer.set_weights([conv_weights, conv_bias])
        else:
            # load conv weights, load batch norm weights
            layer.set_weights([conv_weights])
            batch_norm_layers[current_matching_batch_norm_index].set_weights(
                batch_norm_weights
            )
            current_matching_batch_norm_index += 1

    #  Check if we read the entire darknet file.
    remaining_chars = len(darknet_weight_file.read())
    darknet_weight_file.close()
    assert remaining_chars == 0

    return yolo_model


def get_weights_by_keyword_or_path(weights, model):
    """
    Return weights path for keyword for pretrained model.

    Args:
        weights (str): Path or pretrained model keyword.
        model (tf.keras.Model): Model to load weights into.

    Returns:
        str: Path to the weights to load.
    """
    if (
        weights not in [None, *AVAILABLE_PRETRAINED_WEIGHTS_OPTIONS]
        and not Path(weights).is_file()
    ):
        raise ValueError(
            f"`weights` argument should either be in {AVAILABLE_PRETRAINED_WEIGHTS_OPTIONS}, "
            "a path to a valid .h5 file or None (random initialization)"
        )

    if weights is None:
        return None

    if Path(weights).is_file():
        return weights

    return get_weights_by_keyword(weights, model)


def get_weights_by_keyword(weights, model):
    """
    Access pretrained weights based on keyword. Accepted keywords are: ["darknet"].

    Args:
        weights (str): Path or pretrained model keyword.
        model (tf.keras.Model): Model to load weights into.

    Returns:
        str: Path to the weights to load.
    """
    if weights == "darknet":
        return get_darknet_weights_path_by_download(model)

    return None


def get_darknet_weights_path_by_download(model):
    """
    Return Darknet weights path pretrained on COCO.

    Args:
        model (tf.keras.Model): Model to load weights into.

    Returns:
        str: Path to the weights to load.
    """
    if DARKNET_WEIGHTS_PATH.is_file():
        return DARKNET_WEIGHTS_PATH

    darknet_weights_path = download_darknet_weights(model)

    return darknet_weights_path


def download_darknet_weights(yolov4_model):
    """
    Download original Darknet yolov4.weights file from Google Drive and
    transforms it to a compatible .h5 format

    Args:
        yolov4_model (tf.keras.Model): YOLOv4 model
    """
    if not TF2_YOLOV4_DEFAULT_PATH.is_dir():
        TF2_YOLOV4_DEFAULT_PATH.mkdir()

    is_darknet_original_weights_available = DARKNET_ORIGINAL_WEIGHTS_PATH.is_file()

    if not is_darknet_original_weights_available:
        print("Download original Darknet weights")
        download_file_from_google_drive(
            YOLOV4_DARKNET_FILE_ID,
            DARKNET_ORIGINAL_WEIGHTS_PATH,
            target_size=YOLOV4_DARKNET_FILE_SIZE,
        )

    print("Converting original Darknet weights to .h5 format")
    yolov4 = load_darknet_weights_in_yolo(
        yolov4_model, str(DARKNET_ORIGINAL_WEIGHTS_PATH)
    )
    yolov4.save_weights(str(DARKNET_WEIGHTS_PATH))

    return DARKNET_WEIGHTS_PATH

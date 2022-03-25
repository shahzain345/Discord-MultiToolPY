import os
import requests
import cv2
import numpy as np
try:
    import hcaptcha
except:
    os.system("pip install -U git+https://github.com/1337Syntax/py-hcaptcha")
# ===== image detector ====== # https://github.com/QIN2DIM/hcaptcha-challenger/blob/7fc13d9e193ea8cb527af91d3bbf1737d1ac10c4/src/services/hcaptcha_challenger/solutions/yolo.py#L13


class YOLO:
    """YOLO model for image classification"""

    def __init__(self, dir_model, onnx_prefix: str = "yolov5s6"):
        self.dir_model = "./model" if dir_model is None else dir_model
        self.onnx_prefix = (
            "yolov5s6"
            if onnx_prefix not in ["yolov5m6", "yolov5s6", "yolov5n6"]
            else onnx_prefix
        )

        self.onnx_model = {
            "name": f"{self.onnx_prefix}(onnx)_model",
            "path": os.path.join(self.dir_model, f"{self.onnx_prefix}.onnx"),
            "src": f"https://github.com/QIN2DIM/hcaptcha-challenger/releases/download/model/{self.onnx_prefix}.onnx",
        }

        self.flag = self.onnx_model["name"]

        # COCO namespace
        self.classes = [
            "person",
            "bicycle",
            "car",
            "motorbike",
            "aeroplane",
            "bus",
            "train",
            "truck",
            "boat",
            "traffic light",
            "fire hydrant",
            "stop sign",
            "parking meter",
            "bench",
            "bird",
            "cat",
            "dog",
            "horse",
            "sheep",
            "cow",
            "elephant",
            "bear",
            "zebra",
            "giraffe",
            "backpack",
            "umbrella",
            "handbag",
            "tie",
            "suitcase",
            "frisbee",
            "skis",
            "snowboard",
            "sports ball",
            "kite",
            "baseball bat",
            "baseball glove",
            "skateboard",
            "surfboard",
            "tennis racket",
            "bottle",
            "wine glass",
            "cup",
            "fork",
            "knife",
            "spoon",
            "bowl",
            "banana",
            "apple",
            "sandwich",
            "orange",
            "broccoli",
            "carrot",
            "hot dog",
            "pizza",
            "donut",
            "cake",
            "chair",
            "sofa",
            "pottedplant",
            "bed",
            "diningtable",
            "toilet",
            "tvmonitor",
            "laptop",
            "mouse",
            "remote",
            "keyboard",
            "cell phone",
            "microwave",
            "oven",
            "toaster",
            "sink",
            "refrigerator",
            "book",
            "clock",
            "vase",
            "scissors",
            "teddy bear",
            "hair drier",
            "toothbrush",
        ]

    def download_model(self):
        """Download model and weight parameters"""
        if not os.path.exists(self.dir_model):
            os.mkdir(self.dir_model)
        if os.path.exists(self.onnx_model["path"]):
            return

        if not self.onnx_model["src"].lower().startswith("http"):
            raise ValueError from None

        print(
            f"Downloading {self.onnx_model['name']} from {self.onnx_model['src']}")
        with requests.get(self.onnx_model["src"], stream=True) as response, open(
            self.onnx_model["path"], "wb"
        ) as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    def detect_common_objects(self, img_stream, confidence=0.4, nms_thresh=0.4):
        """
        Object Detection
        Get multiple labels identified in a given image
        :param img_stream: image file binary stream
             with open(img_filepath, "rb") as file:
                data = file.read()
             detect_common_objects(img_stream=data)
        :param confidence:
        :param nms_thresh:
        :return: bbox, label, conf
        """
        np_array = np.frombuffer(img_stream, np.uint8)
        img = cv2.imdecode(np_array, flags=1)
        height, width = img.shape[:2]

        blob = cv2.dnn.blobFromImage(
            img, 1 / 255.0, (128, 128), (0, 0, 0), swapRB=True, crop=False
        )
        self.download_model()

        net = cv2.dnn.readNetFromONNX(self.onnx_model["path"])

        net.setInput(blob)

        class_ids = []
        confidences = []
        boxes = []

        outs = net.forward()

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                max_conf = scores[class_id]
                if max_conf > confidence:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - (w / 2)
                    y = center_y - (h / 2)
                    class_ids.append(class_id)
                    confidences.append(float(max_conf))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence, nms_thresh)

        return [str(self.classes[class_ids[i]]) for i in indices]

    def solution(self, img_stream: bytes, label: str, **kwargs) -> bool:
        """Implementation process of solution"""
        confidence = kwargs.get("confidence", 0.4)
        nms_thresh = kwargs.get("nms_thresh", 0.4)
        labels = self.detect_common_objects(img_stream, confidence, nms_thresh)
        return bool(label in labels)


def createChallenge(sitekey, host):
    try:
        ch = hcaptcha.Challenge(
            site_key=sitekey,
            site_url=f"https://{host}"
        )
        aliases = {
            "airplane": "aeroplane",
            "аirplane": "aeroplane",
            "motorbus": "bus",
            "mοtorbus": "bus",
            "truck": "truck",
            "truсk": "truck",
            "motorcycle": "motorbike",
            "boat": "boat",
            "bicycle": "bicycle",
            "train": "train",
            "vertical river": "vertical river",
            "airplane in the sky flying left": "airplane in the sky flying left",
        }
        if ch.token:
            return ch.token
        question = ch.question["en"]
        word = question.split("containing an ")[1] if "an" in question else question.split("containing a ")[1]
        if word == "seaplane":
            return createChallenge(sitekey, host)
        yolo = YOLO(dir_model=None)
        for tile in ch:
            res = yolo.solution(img_stream=requests.get(
                tile.image_url).content, label=aliases[word])
            if res:
                ch.answer(tile)
        try:
            token = ch.submit()
            return token
        except Exception as e:
            #print(e)
            return createChallenge(sitekey, host)
    except Exception as e:
        #print(e)
        return createChallenge(sitekey, host)


if __name__ == "__main__":
    token = createChallenge(
        "4c672d35-0701-42b2-88c3-78380b0db560", "discord.com")
    print(token)

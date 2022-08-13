import torch
import numpy as np
import cv2
# import pafy
import time

width = 960
height = 720

class ObjectDetection:
    """
    class implemnets yolo5 model to make inferences on webcam using OpenCV
    """

    def __init__(self, model_name):

        self.model = self.load_model(model_name)
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("\n\nDevice Used:", self.device)

    def get_video_capure(self):
        """
            Creates a new video streaming object to extract video frame by frame to make prediction on.
            :return: opencv2 video capture object, with lowest quality frame available for video.
            """

    def load_model(self, model_name):
        """
        loads Yolot model from pytorch hub.
        :return: Trained pytorch model
        """

        if model_name:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolov5 model
        :param frame: input frame in numpy/list/tuple format.
        :return: labels and Coordinates of object detected by model in the frame.
        """

        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)

        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :retrun: corresponding string label
        """

        return self.classes[int(x)]

    def plot_boxes(self, results, frame):

        """
        Takes frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """

        sayac = 0
        hedef_orani = 0
        hedef_orta_X = 0
        hedef_orta_Y = 0
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        cv2.rectangle(frame, (width*0.25, height*0.1), (width*0.75, height*0.9), (255, 0, 0), 2)
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.6:
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
                hedef_orani = (100 * (x2 - x1)) / 960
                hedef_orta_X = (x2 + x1) / 2
                hedef_orta_Y = (y2 + y1) / 2
                bgr = (0, 0, 255)
                cv2.circle(frame, (int(hedef_orta_X), int(hedef_orta_Y)), 2, bgr, 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, "HEDEF: {:.2f}".format(row[4]), (x1 + 10, y1 - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
                if 240 < x1 and 54 < y1 and x2 < 720 and y2 < 486 and hedef_orani > 5:
                    for sayac in range(0, 4):
                        time.sleep(1)
                        sayac += 1

        cv2.putText(frame, 'Hedef Oran : %{:.2f}'.format(hedef_orani), (20, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(frame, 'Sayac : {:.0f} s'.format(sayac), (20, 495), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        return frame

    def __call__(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        while cap.isOpened():

            ret, frame = cap.read()
            print('Resolution: ' + str(frame.shape[0]) + ' x ' + str(frame.shape[1]))
            if not ret:
                break

            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)

            cv2.putText(frame, 'Gorev : Savasan', (20, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, 'Mod : Otonom', (20, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, 'Hiz : 12.5 m/s', (20, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, 'Irtifa : 42 m', (20, 405), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame, 'Kilitlenme : 2', (20, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            cv2.imshow('YOLOv5 Detection', frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()


# create a new object execute.k
detection = ObjectDetection(model_name='yolov5x.pt')
detection()

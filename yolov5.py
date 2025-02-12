import cv2
import torch

yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5l',
                            device='cuda:0' if torch.cuda.is_available() else 'cpu')  # 예측 모델
yolo_model.classes = [0]  # 예측 클래스 (사람)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 20.0, (frame.shape[1], frame.shape[0]))

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    results = yolo_model(frame)
    results_refine = results.pandas().xyxy[0].values
    nms_human = len(results_refine)
    if nms_human > 0:
        for bbox in results_refine:
            start_point = (int(bbox[0]), int(bbox[1]))
            end_point = (int(bbox[2]), int(bbox[3]))

            frame = cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 3)
    cv2.imshow("Video streaaming", frame)
    if cv2.waitKey(1) == ord("q"):
        break

    out.write(frame)
out.release()
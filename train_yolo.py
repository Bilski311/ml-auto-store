from ultralytics import YOLO


# Load a model
model = YOLO("yolov8n.pt")
# Use the model
model.train(data="config.yaml", epochs=10, batch=-1)
metrics = model.val()
results = model("https://ultralytics.com/images/bus.jpg")
path = model.export(format="onnx")

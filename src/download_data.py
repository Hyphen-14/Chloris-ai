from roboflow import Roboflow
rf = Roboflow(api_key="IbNv43xxhSDW6aWYIsqG")
project = rf.workspace("nick-speer-ofaik").project("plantdoc-dxufs")
version = project.version(7)
dataset = version.download("yolov8", location = "datasets")
                
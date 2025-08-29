"""
验证
Val 模式用于在 YOLO 模型训练完成后对其进行验证。
在此模式下，模型会在验证集上进行评估，以衡量其准确性和泛化性能。
此模式可用于调整模型的超参数，以提高其性能。
"""
if __name__ == '__main__':
    """训练后验证"""
    from ultralytics import YOLO

    # Load a YOLO model
    model = YOLO("yolo11n.yaml")

    # Train the model
    model.train(data="coco8.yaml", epochs=5)

    # Validate on training data
    model.val()


    """在其他数据集上验证"""
    # from ultralytics import YOLO
    #
    # # Load a YOLO model
    # model = YOLO("yolo11n.yaml")
    #
    # # Train the model
    # model.train(data="coco8.yaml", epochs=5)
    #
    # # Validate on separate data
    # model.val(data="path/to/separate/data.yaml")
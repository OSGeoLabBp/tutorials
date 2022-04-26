import numpy as np
import cv2
import sys
import os.path

def classify_img(image):
    """ detect object on image using ImageNet """
    # create blob from image
    blob = cv2.dnn.blobFromImage(image=image, scalefactor=0.01, size=(224, 224),
                                 mean=(104, 117, 123))
    # set the input blob for the neural network
    model.setInput(blob)
    # forward pass image blog through the model
    outputs = model.forward()
    final_outputs = outputs[0]
    # make all the outputs 1D
    final_outputs = final_outputs.reshape(1000, 1)
    # get the class label
    label_id = np.argmax(final_outputs)
    # convert the output scores to softmax probabilities
    probs = np.exp(final_outputs) / np.sum(np.exp(final_outputs))
    # get the final highest probability
    final_prob = np.max(probs) * 100.
    # map the max confidence to the class label names
    out_name = class_names[label_id]
    out_text = f"{out_name}, {final_prob:.1f} %"
    return out_text

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} image')
    sys.exit()
# read the ImageNet class names
with open('data/classification_classes_ILSVRC2012.txt', 'r') as f:
   image_net_names = f.read().split('\n')
# final class names (just the first word of the many ImageNet names for one image)
class_names = [name.split(',')[0] for name in image_net_names]
model = cv2.dnn.readNet(model='data/DenseNet_121.caffemodel',
                        config='data/DenseNet_121.prototxt',
                        framework='Caffe')
i = 1
view_img = False
if sys.argv[1] == '-v':
    i = 2
    view_img = True
# load the image from disk
for img_name in sys.argv[i:]:
    img = cv2.imread(img_name)
    if img is None:
        print(f'Image {img_name} not opened')
        continue
    label = classify_img(img)
    width = img.shape[1]
    height = img.shape[0]
    w1 = 600
    h1 = int(w1 / width * height)
    img1 = cv2.resize(img, (w1, h1))
    # put the class name text on top of the image
    cv2.putText(img1, label, (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255), 2)
    if view_img:
        cv2.imshow('Image', img1)
        cv2.waitKey(0)
    else:
        path_name = os.path.split(img_name)
        name_ext = os.path.splitext(path_name[1])
        label_parts = label.split(',')
        out_name = os.path.join(path_name[0],
                                label_parts[0] + '_' + name_ext[0] + name_ext[1])
        cv2.imwrite(out_name, img1)

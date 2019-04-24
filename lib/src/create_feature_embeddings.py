# MIT License
#
# Copyright (c) 2016 David Sandberg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import argparse
import facenet
#ppipimport lfw
import os
import sys
import math
import tqdm
from scipy.misc import imread
from sklearn import metrics
from scipy.optimize import brentq
from scipy import interpolate
import PIL.Image as Image
import numpy as np
import pickle
from keras.preprocessing.image import load_img, img_to_array


def load_image(img, do_random_crop, do_random_flip, image_size, do_prewhiten=True):
    #nrof_samples = len(image_paths)
    images = np.zeros((1, image_size, image_size, 3))
    #for i in range(nrof_samples):
    img = imread(img)
    #img = misc.imresize(img,(160,160,3))
    if img.ndim == 2:
            img = to_rgb(img)
    if do_prewhiten:
            img = facenet.prewhiten(img)
    img = facenet.crop(img, do_random_crop, image_size)
    img = facenet.flip(img, do_random_flip)
    images[:,:,:,:] = img
    return images

def main(args):
    with tf.Graph().as_default():

        with tf.Session() as sess:

            # Get the paths for the corresponding pre-aligned images
            r = []
            train_path= os.path.join('/Users/cindybishop/Documents/Face_Recognition/lib/data/humans_mtcnn/')
            for root, dirs, files in os.walk(train_path):
                for name in files:
                    if 'png' in name:
                        print(name)
                        r.append(os.path.join(root, name))

            paths = r
            # np.save("images.npy",paths)
            # Load the model
            facenet.load_model(args.model)

            # Get input and output tensors --symbolic
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

            image_size = args.image_size
            embedding_size = embeddings.get_shape()[1]
            extracted_dict = {}

            #plt.figure(figsize=(20, 20))
            # Run forward pass to calculate embeddings
            for i, filename in enumerate(paths):

                images = load_image(filename, False, False, image_size)
                feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                feature_vector = sess.run(embeddings, feed_dict=feed_dict)
                extracted_dict[filename] = feature_vector
                if (i % 100 == 0):
                    print("completed", i, " images")



            #for i in extracted_dict:
            #    tsne = TSNE(n_components=len(extracted_dict), random_state=0)
            #    reduced = tsne.fit_transform(i)
            #    plt.scatter(i[0], i[1], label=i.keys())

            #plt.legend()
            #plt.show()

            with open('extracted_dict.pickle', 'wb') as f:
                pickle.dump(extracted_dict, f)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--lfw_batch_size', type=int,
                        help='Number of images to process in a batch in the LFW test set.', default=100)
    parser.add_argument('--model', type=str, default='/Users/cindybishop/Documents/Face_recognition/lib/src/ckpt/20180408-102900.pb',
                        help='Could be either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file')
    parser.add_argument('--image_size', type=int,
                        help='Image size (height, width) in pixels.', default=160)

    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
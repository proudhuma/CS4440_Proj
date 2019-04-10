'''
## Installing latest version of TF-slim

TF-Slim is available as tf.contrib.slim via TensorFlow 1.0. 
To test that your installation is working, execute the following command; it should run without raising any errors.

python -c "import tensorflow.contrib.slim as slim; eval = slim.evaluation.evaluate_once"


## Installing the TF-slim image models library

To use TF-Slim for image classification, you also have to install the TF-Slim image models library, which is not part of the core TF library. To do this, check out the tensorflow/models repository as follows:

cd $HOME/workspace
git clone https://github.com/tensorflow/models/


This will put the TF-Slim image models library in $HOME/workspace/models/research/slim. (It will also create a directory called models/inception, which contains an older version of slim; you can safely ignore this.)

To verify that this has worked, execute the following commands; it should run without raising any errors.

cd $HOME/workspace/models/research/slim
python -c "from nets import cifarnet; mynet = cifarnet.cifarnet"

'''

import sys,cv2,os,glob

tf_path = '/Users/workspace/tensorflow/'
sys.path.append(tf_path)

#Load the definitions of Inception-Resnet-v2 architecture
import tensorflow as tf
import numpy as np
import tensorflow.contrib.slim as slim
from nets.inception_resnet_v2 import inception_resnet_v2, inception_resnet_v2_arg_scope


#The pretrained model accepts size of 299x299 images
HEIGHT = 299
WIDTH = 299
CHANNELS = 3

# Create Graph

def read_image(image_folder,debug=0):
   if not os.path.exists(image_folder):
      print("Error: Image folder does not exist:", image_folder)
      sys.exit(0)

   images_paths = sorted(glob.glob(os.path.join(image_folder + '/*')))

   if not len(images_paths):
      print("No images found in folder")
      sys.exit(0)

   graph = tf.Graph()
   with graph.as_default():

      # Create a placeholder to pass the input image
      img_tensor = tf.placeholder(tf.float32, shape=(len(images_paths), HEIGHT, WIDTH, CHANNELS))

      # Scale the image inputs to {+1, -1} from 0 to 255
      img_scaled = tf.scalar_mul((1.0/255), img_tensor)
      img_scaled = tf.subtract(img_scaled, 0.5)
      img_scaled = tf.multiply(img_scaled, 2.0)

      # load Graph definitions
      with slim.arg_scope(inception_resnet_v2_arg_scope()):
         logits, end_points = inception_resnet_v2(img_scaled, is_training=False)

      # predict the class
      predictions = end_points['Predictions']

   #Pre-processing images_paths
   final_images = []
   for image in images_paths:
      img = cv2.imread(image)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      img = cv2.resize(img, (WIDTH, HEIGHT))
      final_images.append(img)


   # make the input size [BATCH, WIDTH, HEIGHT, CHANNELS] for the network
   final_images = np.squeeze(np.expand_dims(final_images, axis=0))

   #for labels of imagenet 
   sys.path.append(tf_path + 'models/research/slim')
   from datasets import imagenet

   # Inception resnet v2 model

   checkpoint_path = './checkpoints/'
   model_name = 'inception_resnet_v2_2016_08_30'
   checkpoint_file = checkpoint_path + model_name +'.ckpt'

   with tf.Session(graph=graph) as sess:

      saver = tf.train.Saver()
      saver.restore(sess, checkpoint_file)

      pred_prob= sess.run(predictions, feed_dict={img_tensor:final_images})

      # Getting the top 5 classes of the imagenet database
      image_results = dict()

      for file_index, p in enumerate(pred_prob):

         sorted_inds = [i[0] for i in sorted(enumerate(-p), key=lambda x:x[1])]

         names = imagenet.create_readable_names_for_imagenet_labels()

         probability_tag = p[sorted_inds[0]]
         name_tag = names[sorted_inds[0]]
         image_results[images_paths[file_index]] = (name_tag, probability_tag)
         
         if debug:
            print("\nResult:", images_paths[file_index])
            for i in range(5):
               index = sorted_inds[i]
               print('{:.2%} => [{}]'.format(p[index], names[index]))

      return image_results


if __name__ == '__main__':
   image_folder = './images/'

   image_results = read_image(image_folder,debug=1)
   print(image_results)
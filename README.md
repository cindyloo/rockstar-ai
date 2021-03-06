# RockStar AI

<img src="https://github.com/cindyloo/rockstar-ai/blob/master/server/static/images/spock_rock.png" />

RockStar AI is a speculative social media platform in which identity is not connected to one's physical face but rather to one's own "Rockelganger" or "spirit rock." Since most facial recognition systems are trained solely on humans faces (and sometimes cats), rock faces -or any other heterogenous set of images - cannot be detected, identified nor tracked. Exposing the rigidity of facial detection and recognition softwares, its dependence on specific training sets and the now pervasive identification and surveillance of individuals should provoke great concern. The digital world depends on conforming behaviors and static principles, and we should be cautious of reductive representation, especially when that representation is of ourselves.

Humans have an innate ability to see faces in organic as well as inorganic material. This capability is something fairly difficult to replicate in machine learning algorithms. In this way, I expose the constraints with training sets utilized by machine learning algorithms by illustrating how close (or not) CycleGans and style transfers can get to matching human faces to something as diverse and disparate as rocks. 

The training set is sourced from a museum outside of Tokyo called "The Museum of Rocks that Look Like Faces." 
<img src="https://github.com/cindyloo/rockstar-ai/blob/master/rock_faces.jpg" >

" Once upon a time, there was a man named Shozo Hayama-san. He saw faces in many things, especially the rocks along the river in his town.  He loved these rocks and surrounded himself with them.  Over time he had many hundreds of these rock friends. When he passed away, his rocks stayed behind, as rocks usually do." 

Shozo Hayam-san gathered these rocks over 50 years and in fact started up a museum showcasing these rocks of humanity. As he has since passed away, his daughter runs the museum. This project serves as both a reminder and a warning for our desire to systematize the natural world and what goes missing in that pursuit. Can we emulate Shozo Hayama-san's vision? Should we even try?



As such, this project from MIT's Civic Media serves a few purposes:

1) To provoke discussion and evaluation between human pattern-matching capability to that of machine-learning algorithms regarding facial detection and recognition capabilities.

2) To work towards a dataset and model that can approximate the human capability to see faces in non-human and inorganic objects.

3) To provide a speculative social media platform in which identity is not connected to one's physical face as much as it is to a "Rockelganger." In fact, a side benefit is the 'identity-scrambling' capability of the Rockelganger. Since facial recognition systems are trained solely on humans faces (and sometimes [cats](https://www.pyimagesearch.com/2016/06/20/detecting-cats-in-images-with-opencv/)), rock faces cannot be tracked.

Let us see how well or poorly we can train a model to see all different sizes, colors and shapes of faces! We'll go for the lower-hanging approach first:

A light weight face recognition implementation using a pre-trained facenet model. Most of the code is taken from David Sandberg's  [facenet](https://github.com/davidsandberg/facenet) repository.

## I followed Vinayak Kailas' excellent [tutorial](https://github.com/vinayakkailas/Face_Recognition) to utilize David Sandberg's FaceNet 
## Steps to follow:
1. Create a dataset of faces for each person and arrange them in below order
```
root folder  
│
└───Person 1
│   │───IMG1
│   │───IMG2
│   │   ....
└───Person 2
|   │───IMG1
|   │───IMG2
|   |   ....
```
2. Align the faces using MTCNN or dllib. Please use the scripts available in lib/src/align. For this project i aligned faces using MTCNN (eg: 
python -m align.align_dataset_mtcnn ../data/humans ../data/humans_mtcnn --image_size 160 --margin 32 --random_order --gpu_memory_fraction 0.25
). You should default to 160 as FaceNet uses this image size.

[Before alignment]<img src="https://github.com/cindyloo/rockstar-ai/blob/master/lib/data/humans/spock/human_spock_539.jpg"  width="250" height="250" />    [After alignment] <img src="https://github.com/cindyloo/rockstar-ai/blob/master/lib/data/humans_mtcnn/spock/human_spock_539.png"  width="250" height="250" /> 

3. Download [pre-trained-weight](https://drive.google.com/open?id=1R77HmFADxe87GmoLwzfgMu_HY0IhcyBz) ,extract and keep it in lib/src/ckpt folder (for detailed info about availabe weights: [available-weights](https://github.com/davidsandberg/facenet#pre-trained-models)) 
4. Create face/feature embeddings using pre-trained facenet model. Run the below scripts by changing the folder paths.(edit paths in [lines](https://github.com/cindybishop/rockstar-ai/lib/src/create-feature-embeddings.py))
```
  python lib/src/create_face_embeddings.py 
 ```
  Once you run the script succesfully, a pickle file with name embeddings_dict.pickle will be generated inside lib/src folder
 
5. Start the server by running the command
```
  python server/rest-server.py
```
  access the UI using url https://127.0.0.1:5000. It will a video feed, a Rock It! button and then the results appear. Once you click on it, automatically your primary camera will get turned on and start recognizing the faces.
 [RockStar AI implementation] <img src="https://github.com/cindyloo/rockstar-ai/blob/master/server/static/images/output_rockstar_overview.png" width="600" height="600" /> 
 
References:

* Deepface paper https://www.cs.toronto.edu/~ranzato/publications/taigman_cvpr14.pdf
* Facenet paper https://arxiv.org/pdf/1503.03832.pdf
* Pre-trained facenet model https://github.com/davidsandberg/facenet

Additional notes:
We will be pairing more humans to rocks and could use your help! With only 300 human-rock pairings, there isn't a whole lot of variability in the vector space. Please contact me!

Thanks to Damien Henry at Google Arts for the suggestion for Part 1 of this approach: to create human-to-rock pairings with which to train the system


LIVE AT http://www.rockstar-ai.com

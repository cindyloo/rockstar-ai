#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template, send_from_directory
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import sys
import random
import cv2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from server import app
from tensorflow.python.platform import gfile
from six import iteritems
import numpy as np
from lib.src import retrieve
from lib.src.align import detect_face
import tensorflow as tf
import pickle
from tensorflow.python.platform import gfile

auth = HTTPBasicAuth()

global closest_match_filename
global closest_match_rock
global accuracy_eval

closest_match_filename = "nothing"
closest_match_rock = "nothingtoo"
accuracy_eval = 0.0
#==============================================================================================================================
#                                                                                                                              
#    Loading the stored face embedding vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================
with open('/Users/cindybishop/Documents/rockstar-ai/lib/src/extracted_dict.pickle','rb') as f:
	feature_array = pickle.load(f)

model_exp = '/Users/cindybishop/Documents/rockstar-ai/lib/src/ckpt/'
graph_fr = tf.Graph()
sess_fr = tf.Session(graph=graph_fr)

with graph_fr.as_default():
	saverf = tf.train.import_meta_graph(os.path.join(model_exp, 'model-20180408-102900.meta'))
	saverf.restore(sess_fr, os.path.join(model_exp, 'model-20180408-102900.ckpt-90'))
	pnet, rnet, onet = detect_face.create_mtcnn(sess_fr, None)
#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the face recognition from video camera                                                          
#                                                                                                 
#                                                                                                                              
#==============================================================================================================================

def set_data():
    return render_template('main.html', closest_match_filename=closest_match_filename)

@app.route('/get_cropped')
def get_cropped():
	print("in get cropped")
	return "/images/cropped.png"

@app.route('/return_img')
def return_img():
	global closest_match_filename
	return '<img src=' + url_for('static', filename=closest_match_filename) + '>'

@app.route('/get_match')
def get_match():
	print("in get_match")
	full_path = "/images/humans_mtcnn/" + closest_match_filename
	return full_path

@app.route('/rock_it')
def rock_it():
	print("in rock it")
	global closest_match_rock
	global closest_match_filename
	print(closest_match_filename)
	if closest_match_filename not in [None, '']:
		rock_number = closest_match_filename.rsplit("_", 1)[1]
		rock_number = rock_number.split(".")[0] + ".jpg" # take off png and add jpg
		closest_match_rock = "/images/rocks/rocks_" + rock_number
		print(closest_match_rock)
	else:
		closest_match_filename = ""
		closest_match_rock = ""
	return closest_match_rock

@app.route('/facerecognitionLive', methods=['GET', 'POST'])
def face_det():

	closest_match, accuracy = retrieve.recognize_face(sess_fr,pnet, rnet, onet,feature_array)
	print("now save match")
	closest_match = "/".join(closest_match.split('/')[8:])
	global closest_match_filename
	global accuracy_eval
	accuracy_eval = accuracy
	closest_match_filename= closest_match
	print(closest_match_filename)
	rock_it()
	# set_data() # I don't think this does anything. filename is still default "nothing"
	return closest_match_filename

#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():

	return render_template("main.html", closest_match_filename=closest_match_filename, closest_match_rock=closest_match_rock, accuracy_eval=accuracy_eval)
if __name__ == '__main__':
	app.run(debug = True, host= '0.0.0.0')

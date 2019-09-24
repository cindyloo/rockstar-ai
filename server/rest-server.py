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
import datetime

from server import app
from tensorflow.python.platform import gfile
from six import iteritems
import numpy as np
from lib.src import retrieve
from lib.src.align import detect_face
import tensorflow as tf
import pickle
from tensorflow.python.platform import gfile
from PIL import Image
from io import BytesIO, StringIO
import base64
import re

app = Flask(__name__, static_url_path = "")

auth = HTTPBasicAuth()

global closest_match_filename
global closest_match_rock
global accuracy_eval
global current_img

current_img = ''
closest_match_filename = "nothing"
closest_match_rock = "nothingtoo"
accuracy_eval = 0.0
#==============================================================================================================================
#                                                                                                                              
#    Loading the stored face embedding vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================
PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
print(PROJECT_HOME)
IMAGE_FOLDER = 'static/images/'

with open('{}/../lib/src/extracted_dict.pickle'.format(PROJECT_HOME),'rb') as f:
	feature_array = pickle.load(f)

model_exp = '{}/../lib/src/ckpt/20180408-102900'.format(PROJECT_HOME)
graph_fr = tf.Graph()
sess_fr = tf.Session(graph=graph_fr)

pnet, rnet, onet = '', '', ''
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
	return "{}/cropped_{}.png".format(IMAGE_FOLDER,current_img)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['.png']

UPLOAD_FOLDER = '{}/'.format(PROJECT_HOME)
DOWNLOAD_FOLDER = 'rocks_copy';
# route http posts to this method
#@app.route('/send_receive_img', methods=['POST'])
def send_receive_img():
	img = request.files['current_image']

	if img:
		filename = "current_image-{}.jpg".format(datetime.datetime.now()).replace("/","-").replace(" ", "")
		img.save(os.path.join(UPLOAD_FOLDER, filename))
		print("saving ")
		return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True), filename


@app.route('/return_img')
def return_img():
	global closest_match_filename
	return '<img src=' + url_for('static', filename=closest_match_filename) + '>'

@app.route('/get_match')
def get_match():
	print("in get_match")
	full_path = "/images/humans_mtcnn/" + closest_match_filename
	return full_path

@app.route('/get_accuracy')
def get_accuracy():
	print("in accuracy")
	global accuracy_eval
	return '{}'.format(accuracy_eval * 100)

@app.route('/write_suggestions')
def write_suggestion():
	#check input
	print(request.args.get('suggestion'))
	input = request.args.get('suggestion')
	suggestions = open("suggestionbox.log", "a")
	global closest_match_rock
	print(input + 'for \n' + closest_match_rock)
	if re.match('^[a-zA-Z0-9_]+$', input):
		suggestions.write(input + ' for ' + closest_match_rock + '\n')



@app.route('/tag_suggestions')
def tag_suggestion():
	#check input
	print(request.args.get('suggestion'))
	input = request.args.get('suggestion')
	rock_suggestions = open("rockbox.log", "a")
	global random_rock
	print(input + 'for \n' + random_rock)
	if re.match('^[a-zA-Z0-9_]+$', input):
		rock_suggestions.write(input + ' for ' + random_rock + '\n')

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
	global current_img
	response, current_img = send_receive_img()
	#if response is ok, continue
	print("received image {}".format(current_img))
	closest_match, accuracy = retrieve.recognize_face(sess_fr,pnet, rnet, onet,feature_array, current_img)
	print("now save match" )
	closest_match = "/".join(closest_match.split('/')[8:])
	global closest_match_filename
	global accuracy_eval
	accuracy_eval = accuracy
	closest_match_filename= closest_match
	print(closest_match_filename)
	rock_it()
	# set_data() # I don't think this does anything. filename is still default "nothing"
	return closest_match_filename

@app.route("/pet_rocks")
def rock_spirit():
	# get random rock images here and send down?
	return render_template("pet_rocks.html")


@app.route("/about")
def about():
	return render_template("about.html")


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

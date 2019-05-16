/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */

'use strict';

// Put variables in global scope to make them available to the browser console.
const constraints = window.constraints = {
  audio: false,
  video: true
};

const snapshotButton = document.querySelector('button#snapshot');
// const filterSelect = document.querySelector('select#filter');

// Put variables in global scope to make them available to the browser console.
const video = window.video = document.querySelector('video');
const canvas = window.canvas = document.querySelector('canvas');
canvas.width = 600;
canvas.height = 480;


function call_server(dataURL){

var blobBin = atob(dataURL.split(',')[1]);
var array = [];
for(var i = 0; i < blobBin.length; i++) {
    array.push(blobBin.charCodeAt(i));
}
var file=new Blob([new Uint8Array(array)], {type: 'image/png'});


var formdata = new FormData();
formdata.append("current_image", file);
$.ajax({
   url: "facerecognitionLive",
   type: "POST",
   data: formdata,
   processData: false,
   contentType: false,
}).done(function(respond){
        load_new_selfie();
    $(".showFirst").show();
        clear_rocks();
        load_new_matches();
        load_new_rock();
        $("body").css("cursor", "default");
        $("button:hover").css("cursor", "pointer");
    });
}

function clear_rocks() {
    $(".reveal").hide();
}
function load_new_selfie() {
            $.ajax({
                url: 'get_cropped',
            }).done(function (data) {
                console.log(data)
                $("#cropped").attr("src", "/images/cropped.png?" + Date());
            });
        }


function load_new_rock() {
            $.ajax({
                url: 'rock_it',
            }).done(function (data) {
                console.log(data)
                $("#rock").attr("src", data);
            });
        }

        function load_new_matches() {
            $.ajax({
                url: 'get_match',
            }).done(function (data) {
                console.log(data)
                //load_new_rock();
                $("#match").attr("src", data);
            });
        }
function about_page() {
            $.ajax({
                url: 'about',
                type: "GET",
            }).done(function (data) {
            });
        }
$(".reveal").hide();
$(".showFirst").hide();
$("#showVideo").hide();

snapshotButton.onclick = function() {
  // canvas.className = filterSelect.value;
  var img = canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
  $("body").css("cursor", "progress");
  $("button:hover").css("cursor", "progress");
  var dataURL = canvas.toDataURL();
  // also save this ?
  call_server(dataURL);
};

placeholder.onclick = function() {
  // canvas.className = filterSelect.value;
  $("#rock").show();
};



uncoverConnectionButton.onclick = function() {
  // canvas.className = filterSelect.value;
$(".reveal").show();

};


function handleSuccess(stream) {
  window.stream = stream; // make stream available to browser console
  video.srcObject = stream;
}

function handleError(error) {
  if (error.name === 'ConstraintNotSatisfiedError') {
    let v = constraints.video;
    errorMsg(`The resolution ${v.width.exact}x${v.height.exact} px is not supported by your device.`);
  } else if (error.name === 'PermissionDeniedError') {
    errorMsg('Permissions have not been granted to use your camera and ' +
      'microphone, you need to allow the page access to your devices in ' +
      'order for the demo to work.');
  }
  errorMsg(`getUserMedia error: ${error.name}`, error);
}

async function init(e) {
    navigator.mediaDevices.getUserMedia(constraints)
        .then(function(stream) {
            handleSuccess(stream);
            e.target.disabled = true;
        })
          .catch(function(err) {
  handleError(e);
          });
}

init();

navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);
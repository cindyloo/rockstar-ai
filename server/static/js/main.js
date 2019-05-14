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

function call_server(){
    $.ajax({
        url: 'facerecognitionLive',
    }).done(function() {
    });
}
$(".reveal").hide();
$("#showVideo").hide();

snapshotButton.onclick = function() {
  // canvas.className = filterSelect.value;
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
  call_server();
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
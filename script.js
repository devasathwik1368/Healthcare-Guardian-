// =========================
// SYMPTOM PREDICTION
// =========================

function predict(){

let symptoms=document.getElementById("symptoms").value

fetch("/predict",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({symptoms:symptoms})
})

.then(res=>res.json())
.then(data=>{

document.getElementById("result").innerText=data.result

})

}


// =========================
// MEDICAL CHAT
// =========================

function chat(){

let msg=document.getElementById("chatinput").value

fetch("/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({message:msg})
})

.then(res=>res.json())
.then(data=>{

let chatbox=document.getElementById("chatbox")

chatbox.innerHTML += "<p><b>You:</b> "+msg+"</p>"

chatbox.innerHTML += "<p><b>Doctor AI:</b> "+data.reply+"</p>"

document.getElementById("chatinput").value=""

})

}


// =========================
// IMAGE UPLOAD SCAN
// =========================

function upload(){

let file=document.getElementById("file").files[0]

let formData=new FormData()

formData.append("file",file)

document.getElementById("scanResult").innerHTML="🔍 Scanning medical image..."

fetch("/upload",{
method:"POST",
body:formData
})

.then(res=>res.json())
.then(data=>{

document.getElementById("image").src=data.image

document.getElementById("scanResult").innerText=data.result

})

}


// =========================
// CAMERA START
// =========================

let video

function startCamera(){

video=document.getElementById("video")

navigator.mediaDevices.getUserMedia({video:true})
.then(stream=>{

video.srcObject=stream
video.play()

})

}


// =========================
// CAMERA CAPTURE
// =========================

function capture(){

let canvas=document.createElement("canvas")

canvas.width=video.videoWidth
canvas.height=video.videoHeight

let ctx=canvas.getContext("2d")

ctx.drawImage(video,0,0)

let img=canvas.toDataURL()

document.getElementById("scanResult").innerHTML="📷 Capturing and analyzing image..."

fetch("/capture",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({image:img})
})

.then(res=>res.json())
.then(data=>{

document.getElementById("image").src=data.image

document.getElementById("scanResult").innerText=data.result

})

}


// =========================
// VOICE INPUT
// =========================

function voice(){

let recognition=new webkitSpeechRecognition()

recognition.lang="en-US"

recognition.onresult=function(event){

document.getElementById("symptoms").value=event.results[0][0].transcript

}

recognition.start()

}


// =========================
// NEAREST HOSPITAL MAP
// =========================

function findHospitals(){

navigator.geolocation.getCurrentPosition(function(position){

let lat=position.coords.latitude
let lon=position.coords.longitude

let map=L.map("map").setView([lat,lon],13)

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map)

L.marker([lat,lon]).addTo(map)
.bindPopup("📍 Your Location")

})

}


// =========================
// HEALTH HISTORY
// =========================

function loadHistory(){

fetch("/history")
.then(res=>res.json())
.then(data=>{

let html=""

data.forEach(item=>{

html += "<p>"+item.disease+"</p>"

})

document.getElementById("history").innerHTML=html

})

}
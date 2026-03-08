from flask import Flask, render_template, request, jsonify
import os
import base64

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

history = []

# =========================
# MEDICAL DATABASE
# =========================

medical_db = {

"fever":{
"disease":"Viral Fever",
"doctor":"General Physician",
"description":"Viral fever is a common infection caused by viruses. Symptoms include high body temperature, fatigue, headache, and body pain. The infection spreads through air droplets and contact with infected individuals. Proper rest, hydration, and medication help recovery. If fever persists for more than three days, medical consultation is recommended."
},

"cough":{
"disease":"Respiratory Infection",
"doctor":"Pulmonologist",
"description":"Persistent cough may indicate respiratory infection or airway irritation. It may occur due to viral infection, allergy, or pollution exposure. Symptoms include throat irritation, chest discomfort, and mucus production. Drinking warm fluids and avoiding dust may help relieve symptoms. Long lasting cough should be examined by a doctor."
},

"cold":{
"disease":"Common Cold",
"doctor":"General Physician",
"description":"Common cold is a viral infection affecting the nose and throat. Symptoms include sneezing, runny nose, mild fever, and sore throat. It spreads easily through droplets and close contact. Rest, hydration, and warm fluids help relieve symptoms."
},

"skin":{
"disease":"Skin Infection",
"doctor":"Dermatologist",
"description":"Skin infections may occur due to bacteria, fungi, or viruses. Symptoms include redness, itching, swelling, and irritation. Poor hygiene or contaminated surfaces may increase infection risk. Dermatologists treat skin conditions using medications and topical treatments."
},

"bone":{
"disease":"Bone Injury",
"doctor":"Orthopedic Specialist",
"description":"Bone injuries occur due to accidents, falls, or heavy impact. Symptoms include severe pain, swelling, bruising, and difficulty moving the affected area. X-ray imaging helps doctors detect fractures or bone damage. Orthopedic specialists provide treatment and rehabilitation."
},

"headache":{
"disease":"Migraine",
"doctor":"Neurologist",
"description":"Migraine is a neurological condition causing intense headaches. Symptoms include throbbing pain, nausea, dizziness, and sensitivity to light. Stress, dehydration, and lack of sleep may trigger migraines. Proper rest and medication help manage symptoms."
},

"stomach":{
"disease":"Gastritis",
"doctor":"Gastroenterologist",
"description":"Gastritis is inflammation of the stomach lining. Symptoms include abdominal pain, nausea, vomiting, and bloating. It may occur due to infections, spicy foods, or stress. Balanced diet and medication help manage symptoms."
},

"chest":{
"disease":"Possible Cardiac Issue",
"doctor":"Cardiologist",
"description":"Chest pain may indicate heart related conditions. Symptoms include pressure in chest, pain spreading to arms or neck, and breathing difficulty. Immediate medical attention is recommended if symptoms are severe."
}

}

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# SYMPTOM PREDICTION
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    symptoms = request.json["symptoms"].lower()

    for key in medical_db:

        if key in symptoms:

            result = medical_db[key]

            reply = f"""
Disease: {result['disease']}

Description:
{result['description']}

Recommended Doctor:
{result['doctor']}
"""

            history.append({
                "disease":result["disease"],
                "risk":"Medium"
            })

            return jsonify({"result":reply})

    return jsonify({"result":"Symptoms unclear. Please consult a doctor."})


# =========================
# MEDICAL CHAT
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    msg = request.json["message"].lower()

    for key in medical_db:

        if key in msg:

            result = medical_db[key]

            reply = f"""
Possible Condition: {result['disease']}

{result['description']}

Doctor to consult: {result['doctor']}
"""

            return jsonify({"reply":reply})

    return jsonify({"reply":"Please explain your symptoms more clearly."})


# =========================
# IMAGE UPLOAD SCAN
# =========================

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    path = os.path.join(UPLOAD_FOLDER,file.filename)

    file.save(path)

    name = file.filename.lower()

    # X-RAY detection
    if "xray" in name or "bone" in name:

        result = """
Possible Condition: Bone Fracture or Bone Injury

Description:
The uploaded image appears to be related to skeletal imaging such as an X-ray scan. 
Bone fractures occur due to accidents, falls, or strong impact. 
Common symptoms include severe pain, swelling, bruising, and difficulty moving the affected area. 
Medical professionals analyze X-ray scans to identify cracks or breaks in bones. 
Early diagnosis helps prevent further complications.

Recommended Doctor:
Orthopedic Specialist
"""

    # Skin detection
    elif "skin" in name or "rash" in name or "fungal" in name:

        result = """
Possible Condition: Skin Infection or Dermatitis

Description:
The uploaded image appears to show skin irritation or infection. 
Skin conditions may occur due to bacteria, fungi, allergies, or environmental exposure. 
Common symptoms include redness, itching, swelling, and visible patches. 
Dermatologists diagnose skin diseases through examination and tests. 
Early treatment helps prevent spreading of infection.

Recommended Doctor:
Dermatologist
"""

    else:

        result = """
Medical Image Received

Description:
The uploaded medical image has been received successfully. 
Further clinical examination may be required for accurate diagnosis. 
Medical specialists typically analyze images such as X-ray or dermatology scans to determine health conditions.

Recommended Doctor:
General Physician
"""

    return jsonify({
        "image":path,
        "result":result
    })


# =========================
# CAMERA CAPTURE
# =========================

@app.route("/capture", methods=["POST"])
def capture():

    img = request.json["image"]

    data = base64.b64decode(img.split(",")[1])

    path = os.path.join(UPLOAD_FOLDER,"capture.png")

    with open(path,"wb") as f:
        f.write(data)

    result = """
Live Image Captured

Description:
The captured image may indicate a visible medical condition. 
Further medical examination may be required to determine the exact cause. 
Doctors often analyze visual symptoms such as swelling, redness, bruising, or skin changes. 
Consult a healthcare professional if symptoms persist.

Recommended Doctor:
General Physician
"""

    return jsonify({
        "image":path,
        "result":result
    })


# =========================
# HISTORY
# =========================

@app.route("/history")
def history_data():
    return jsonify(history)


# =========================

if __name__ == "__main__":
    app.run(debug=True)
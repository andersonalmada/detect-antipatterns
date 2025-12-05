from flask import Flask, request, jsonify
from collections import Counter

app = Flask(__name__)

def detect_repetitive_messages(data, repetition_threshold=5):
    messages = [log["message"] for log in data]
    counter = Counter(messages)

    repetitive = {msg: count for msg, count in counter.items() if count >= repetition_threshold}

    for log in data:
        if log["message"] in repetitive:
            log["detected"] = True
        else:
            log["detected"] = False
            
    return data

def detect_level(data):
    for item in data:
      if item.get('level') in ("DEBUG", "TRACE") and item["detected"] == False:
        item["detected"] = True
        
    return data

@app.post("/detector")
def detect():
    input_data = request.get_json()        
    input_data = detect_repetitive_messages(data=input_data, repetition_threshold=5)
    input_data = detect_level(data=input_data)
    
    count = sum(1 for x in input_data if x["detected"])       

    response = {
        "analyzed": len(input_data),
        "detected": count,
        "data": input_data
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
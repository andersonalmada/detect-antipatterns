from flask import Flask, request, jsonify
from collections import Counter, defaultdict
from datetime import datetime
import json

app = Flask(__name__)

def group_by_second(logs):
    grouped = defaultdict(list)
    for log in logs:
        ts = datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
        grouped[ts.replace(microsecond=0)].append(log)
    return grouped

def detect_volume_spikes(data, max_kbytes=1):
    """Check if any second has more logs than allowed."""
    grouped = group_by_second(data)

    for second, logs in grouped.items():
        json_kbytes = len(json.dumps(logs).encode("utf-8")) / 1024

        if json_kbytes > max_kbytes:
            for log in logs:
                if log["detected"] == False:                
                    log["detected"] = True
                    log["reason"] = "detect_volume_spikes"

    return data

def detect_repetitive_messages(data, repetition_threshold=5):
    messages = [log["message"] for log in data]
    counter = Counter(messages)

    repetitive = {msg: count for msg, count in counter.items() if count >= repetition_threshold}

    for log in data:
        if log["message"] in repetitive:
            if log["detected"] == False:
                log["detected"] = True
                log["reason"] = "detect_repetitive_messages"
            
    return data

def detect_level(data):
    for item in data:
      if item.get('level') in ("DEBUG", "TRACE") and item["detected"] == False:
        item["detected"] = True
        item["reason"] = "detect_level"
        
    return data

@app.post("/detector")
def detect():
    input_data = request.get_json()
    
    for item in input_data:
        item["detected"] = False
        item["reason"] = ""
    
    input_data = detect_volume_spikes(data=input_data, max_kbytes=1)   
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
from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
from deepface import DeepFace
import base64

app = Flask(__name__)
CORS(app)

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 415

        data = request.json
        image_data = data.get('image', '')

        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400

        # Decode Base64 image data
        try:
            image_data = base64.b64decode(image_data)
        except Exception as e:
            return jsonify({'error': 'Base64 decoding failed: ' + str(e)}), 400

        # Convert byte data to NumPy array and decode image
        try:
            np_array = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError('Image decoding failed.')
        except Exception as e:
            return jsonify({'error': 'Image processing failed: ' + str(e)}), 400

        # Analyze emotion
        try:
            result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
            if isinstance(result, list) and len(result) > 0:
                face_result = result[0]
                dominant_emotion = face_result['emotion']
                if isinstance(dominant_emotion, dict):
                    emotion, confidence = max(dominant_emotion.items(), key=lambda item: item[1])
                    return jsonify({'emotion': emotion})
                else:
                    return jsonify({'error': 'Emotion data format is incorrect.'}), 500
            else:
                return jsonify({'error': 'No face detected.'}), 500
        except Exception as e:
            return jsonify({'error': 'Emotion analysis failed: ' + str(e)}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

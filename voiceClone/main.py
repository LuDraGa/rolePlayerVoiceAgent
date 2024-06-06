from voiceClone import VoiceChanger
from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)
voice_changers = {}

@app.route('/init', methods=['POST'])
def init_voice_changer():
    data = request.json
    base_voice_audioFile = data.get('base_voice')
    target_voice_audioFile = data.get('target_voice')
    if not base_voice_audioFile or not target_voice_audioFile:
        return jsonify({'error': 'base_voice and target_voice both are required'}), 400
    
    instance_id = str(uuid4())
    voice_changer = VoiceChanger(base_voice_audioFile, target_voice_audioFile)
    voice_changers[instance_id] = voice_changer

    return jsonify({'instance_id': instance_id})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    instance_id = data.get('instance_id')
    text = data.get('text')
    output_path = data.get('output_path')
    
    if not instance_id or not output_path:
        return jsonify({'error': 'instance_id and output_path are required'}), 400
    
    voice_changer = voice_changers.get(instance_id)
    if not voice_changer:
        return jsonify({'error': 'Instance not found'}), 404
    
    result = voice_changer.speak(text, output_path)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


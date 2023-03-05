from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import requests
import os

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*":{
        "origins":"*"
    }
})
# @app.error_processor
# def my_error_processor(error):
#     return {
#         'status_code': error.status_code,
#         'message': error.message,
#         'detail': error.detail
#     }, error.status_code, error.headers
    
openai.api_key_path = './key'
transcripts = []



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods = ['POST'])
def home():
    name = request.form['name']
    audio_url = request.form['url']

    r = requests.get(audio_url)

    #print(r.headers.get('content-type'))
    with open('./audio_data/test.wav', 'wb') as test_audio:
        test_audio.write(r.content)

    with open('./audio_data/test.wav' ,'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1",audio_file)

    # # transcript = openai.Audio.transcribe("whisper-1",AUDIO_URL)

    os.remove('./audio_data/test.wav') 
    #print ('\nFile, test.wav', 'The file deletion is successfully completed !!')

    return render_template('index.html', audio_content = transcript['text'], name = name)

@app.route('/transcripts', methods = ['POST'])
def transcript():
    name = {'name': request.json['name']}
    audio_url = {'audioURL': request.json['audioURL']}

    r = requests.get(audio_url['audioURL'])
    
    with open('./audio_data/test.wav', 'wb') as test_audio:
        test_audio.write(r.content)

    with open('./audio_data/test.wav' ,'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1",audio_file)

    os.remove('./audio_data/test.wav') 
    res = {
        'name': name['name'],
        'transcript': transcript['text']
        }
    transcripts.append(res)
    return jsonify(res)

@app.route('/transcripts', methods = ['GET'])
def get_all():
    return transcripts

if __name__ == '__main__':
    app.run(debug=True)
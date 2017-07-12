import io
import json
from pprint import pprint
import os

# Imports the Google Cloud client library
from time import sleep

from google.cloud import speech
from pydub import AudioSegment

from os import listdir
from os.path import isfile, join

import ntpath

from tinytag import TinyTag

from collections import Counter

# Cross-platform compatibility
import platform

if platform.system() == "Windows":
    AudioSegment.converter = "C:\\Users\\User\\Software\\ffmpeg-20170702-c885356-win64-static\\bin\\ffmpeg.exe"

# Constants
RESOURCES = 'resources'
CURRENT_PATH = os.path.dirname(__file__)


# TODO: migrate project to gitlab on Asgard server
def run():
    """
    A method that produces transcripts of speech from audio files using google cloud and pydub
    Returns a list of transcribed speech data
    :return: results (list of Strings)
    """
    # Instantiates a client
    speech_client = speech.Client()

    # Get all files in resources dir
    def get_filepaths(sound_format=str(), if_not_converted=False):
        path = join(CURRENT_PATH, RESOURCES)
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith("." + sound_format.lower())]
        if if_not_converted:
            paths = [join(CURRENT_PATH, RESOURCES, f) for f in onlyfiles if not isfile(join(path, f[:-3] + "flac"))]
        else:
            paths = [join(CURRENT_PATH, RESOURCES, f) for f in onlyfiles]
        return paths

    # Convert WAV to FLAC using pydub library
    def wav2flac(path_list):
        for in_path in path_list:
            song = AudioSegment.from_wav(in_path)
            out_path = in_path[:-3] + "flac"
            # Convert to mono channel as google cloud API works only with mono sound
            song.export(out_path, format="flac", parameters=["-ac", "1"])

    list_filepaths = get_filepaths("WAV", if_not_converted=True)
    wav2flac(list_filepaths)

    # Use flac files to transcribe
    list_filepaths = get_filepaths("FLAC")

    # Loads the audio into memory
    def flacs_to_transcribed_dict(list_paths):
        all_transcripts = dict()
        for path in list_paths:
            with io.open(path, 'rb') as audio_file:
                content = audio_file.read()
                sample = speech_client.sample(content, encoding='FLAC')
                # Detects speech in the audio file
                # TODO: do we need several alternatives or just the best shot? Accuracy improvement issue
                alternatives = sample.recognize('ru', max_alternatives=1)
                results = list()
                for alternative in alternatives:
                    print('Transcript: {}'.format(alternative.transcript))
                    results.append(alternative.transcript)
                file_name = ntpath.basename(path)
                info = dict()
                tag = TinyTag.get(path)
                info['duration_seconds'] = tag.duration
                if len(results) > 1:
                    alter_info = dict()
                    for index, alternative in enumerate(results):
                        alter_info['word_count'] = Counter(alternative.split())
                        alter_info['num_words'] = sum(info['word_count'].values())
                        alter_info['transcript'] = alternative
                        info['alternative'+str(index)] = alter_info
                else:
                    info['word_count'] = Counter(results[0].split())
                    info['num_words'] = sum(info['word_count'].values())
                    info['transcript'] = results[0]
                all_transcripts[file_name] = info
        return all_transcripts

    def create_json_transcript(tscripts=dict(), filename="transcripts.json"):
        tr_path = join(CURRENT_PATH, RESOURCES, filename)
        with open(tr_path, 'w') as outfile:
            json.dump(tscripts, outfile)

    def load_json_transcript(filename="transcripts.json"):
        tr_path = join(CURRENT_PATH, RESOURCES, filename)
        with open(tr_path) as data_file:
            data = json.load(data_file)
        return data

    try:
        tr_json = load_json_transcript()
    except FileNotFoundError as err:
        transcripts = flacs_to_transcribed_dict(list_filepaths)
        create_json_transcript(transcripts)
        tr_json = load_json_transcript()

    pprint(tr_json)

    # TODO: need to implement denoising of transcripts using pipeline found in topic modelling denoising.


if __name__ == '__main__':
    run()

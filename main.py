import io
import json
import os

# Imports the Google Cloud client library
from time import sleep

from google.cloud import speech
from pydub import AudioSegment

from os import listdir
from os.path import isfile, join

import ntpath

RESOURCES = 'resources'


def run():
    """
    A method that produces transcripts of speech from audio files using google cloud and pydub
    Returns a list of transcribed speech data
    :return: results (list of Strings)
    """
    # Instantiates a client
    speech_client = speech.Client()

    # Get all files in resources dir
    def get_filepaths(sound_format=str()):
        path = join(os.path.dirname(__file__), RESOURCES)
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith("." + sound_format.lower())]
        paths = [join(os.path.dirname(__file__), RESOURCES, f) for f in onlyfiles]
        return paths

    # Convert WAV to FLAC using pydub library
    def wav2flac(path_list):
        for in_path in path_list:
            song = AudioSegment.from_wav(in_path)
            out_path = in_path[:-3] + "flac"
            # Convert to mono channel as google cloud API works only with mono sound
            song.export(out_path, format="flac", parameters=["-ac", "1"])

    list_filepaths = get_filepaths("WAV")
    wav2flac(list_filepaths)

    # Use flac files to transcribe
    list_filepaths = get_filepaths("FLAC")

    # Loads the audio into memory
    def transcribe_all_flacs(list_paths):
        all_transcripts = dict()
        for path in list_paths:
            with io.open(path, 'rb') as audio_file:
                content = audio_file.read()
                sample = speech_client.sample(content, encoding='FLAC')
                # Detects speech in the audio file
                alternatives = sample.recognize('ru')
                results = list()
                for alternative in alternatives:
                    print('Transcript: {}'.format(alternative.transcript))
                    results.append(alternative.transcript)
                file_name = ntpath.basename(path)
                all_transcripts[file_name] = results
        return all_transcripts

    transcripts = transcribe_all_flacs(list_filepaths)
    transcripts_filename = "transcripts.json"
    tr_path = join(os.path.dirname(__file__), RESOURCES, transcripts_filename)
    with open(tr_path, 'w') as outfile:
        json.dump(transcripts, outfile)

        # TODO: debug loading from json so that russian text is displayed correctly


if __name__ == '__main__':
    run()

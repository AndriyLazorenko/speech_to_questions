import io
import os

# Imports the Google Cloud client library
from time import sleep

from google.cloud import speech
from pydub import AudioSegment


def run():
    """
    A method that produces transcripts of speech from audio files using google cloud and pydub
    Returns a list of transcribed speech data
    :return: results (list of Strings)
    """
    # Instantiates a client
    speech_client = speech.Client()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'russian.wav')

    # Convert WAV to FLAC using pydub library
    song = AudioSegment.from_wav(file_name)
    # Convert to mono channel as google cloud API works only with mono sound
    song.export("resources/russian.flac", format="flac", parameters=["-ac", "1"])

    # Use new file name of flac file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'russian.flac')
    # print(file_name)

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        sample = speech_client.sample(
            content,
            encoding='FLAC')

    # Detects speech in the audio file
    alternatives = sample.recognize('ru')

    results = list()
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
        results.append(alternative.transcript)
    return results


if __name__ == '__main__':
    run()

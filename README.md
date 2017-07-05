## Speech to Questions software prototype
#### Dependencies
To start working with the repository, go through the following steps first:

- Install google cloud speech recognition API.

In your conda env, run the following:

`pip install --upgrade pip` 

`pip install --upgrade setuptools`

`pip install --upgrade google-cloud-speech`

`pip install -r requirements.txt`

- Follow the guide using link to setup google cloud SDK:
https://cloud.google.com/sdk/docs/
- Authenticate in google cloud using `gcloud init`
- Authenticate app using `gcloud auth application-default login`
##### Windows only additional step
When using Windows, need to install `ffmpeg` lib. 

Follow the guide: http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/

After installing `ffmpeg` according to the guide, need to add path to `ffmpeg.exe` file as follows:

`AudioSegment.converter = "C:\\Users\\User\\Software\\ffmpeg-20170702-c885356-win64-static\\bin\\ffmpeg.exe"`

right after pydub initialization. After that, code should compile

#### Running code
Run code from main.py to receive transcribed text from WAV file in resources (russian.wav)

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from secret import IBM_KEY, IBM_URL
import os

IBM_KEY=os.environ.get('IBM_KEY')
IBM_URL=os.environ.get('IBM_URL')

# IBM Watson: text-to-speech
authenticator = IAMAuthenticator(IBM_KEY)
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)
URL=IBM_URL

class IBM_Text_To_Speech():
    def __init__(self, text, filename):
        self.text=text
        self.filename=filename

    def create_speech(self):

        text_to_speech.set_service_url(URL)

        with open(f'static/audios/{self.filename}.wav', 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    self.text,
                    voice='en-US_AllisonV3Voice',
                    accept='audio/wav'        
                ).get_result().content)
import boto3


class SpeechSyntetizer:

    def __init__(self, access_key, secret_key, voice_id="Vitoria", output_format="ogg_vorbis", language_code="pt-BR"):
        super().__init__(self)
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__voice_id = voice_id,
        self.__output_format = output_format,
        self.__language_code = language_code,

    def get_speech(self, ssml):
        polly_client = boto3.Session(
            aws_access_key_id=self.__access_key,
            aws_secret_access_key=self.__secret_key,
            region_name='us-west-2').client('polly')
        response = polly_client.synthesize_speech(VoiceId=self.__voice_id,
                                                  OutputFormat=self.__output_format,
                                                  LanguageCode=self.__language_code,
                                                  TextType='ssml',
                                                  Text=ssml)

        return response['AudioStream'].read()

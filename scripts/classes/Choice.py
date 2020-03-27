import json

class Choice:

    def __init__(self, option, chat_id):
        self.__option = option;
        self.__chat_id = chat_id;

    def get_option(self):
        return self.__option

    def get_chat_id(self):
        return self.__chat_id

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

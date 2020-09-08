import os
import yaml

class SlackChatBotUtils(object):

    @staticmethod
    def load_yaml_file(input_path:str) -> dict:
        with open(input_path, 'r') as fh:
            return yaml.load(fh, Loader=yaml.FullLoader)

    @staticmethod
    def load_yaml_files(input_path:str) -> []:
        retval = []
        # FIXME: Add some error handling if input_path is not a dir
        for file in os.listdir(input_path):
            if file.endswith('.yaml'):
                input_file_path = os.path.join(input_path, file)
                with open(input_file_path, 'r') as fh:
                    retval.append(yaml.load(fh, Loader=yaml.FullLoader))

        return retval
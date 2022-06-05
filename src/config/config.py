import yaml

def load_config():
    with open("/Users/nurimateos/PycharmProjects/forecasting/src/config/config.yaml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
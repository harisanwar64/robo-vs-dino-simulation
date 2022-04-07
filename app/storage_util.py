import os
import json


class StorageUtility:

    def write_json(self, updated_json, json_file):
        """write entity for robot or dinosaur to backend (json file) for permanent storage"""

        try:
            if os.path.exists(json_file):
                with open(json_file, 'w') as outfile:
                    outfile.write(str(updated_json))
        except Exception as e:
            print(e)

    def read_json(self, json_file):
        """read entity for robot or dinosaur from backend (json file)"""

        try:
            if os.path.exists(json_file):
                with open(json_file) as file:
                    return json.load(file)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    storage = StorageUtility()
    # print(storage.read_json('./simulation_data/robo_vs_dino.json'))



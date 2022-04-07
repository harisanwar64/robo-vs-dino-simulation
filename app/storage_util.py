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

    def update_entity_by_coordinate_value(self, x_cord, y_cord, direction, attack, json_file):
        """ Update entity attribute i.e. change direction, attack flag etc. Write new updates to backend (json)"""

        json_entities = self.read_json(json_file)
        for entity in json_entities:
            if entity.get('x_cord', None) and entity.get('x_cord', None) == x_cord and entity.get('y_cord', None) and entity.get('y_cord', None) == y_cord:
                entity['direction'] = direction
                entity['attack'] = attack
                self.write_json(json.dumps(json_entities), json_file)
                return json_entities


    def remove_entity_by_coordinate_value(self, x_cord, y_cord, json_file):
        """This method remove entity i.e. dinosaur after an attack by robot. Also update these changes to backend
        (json file). """

        json_entities = self.read_json(json_file)
        for i, entity in enumerate(json_entities):
            try:
                if entity['x_cord'] == x_cord and entity['y_cord'] == y_cord and entity['type'] != 'R':
                    json_entities.pop(i)
                    self.write_json(json.dumps(json_entities), json_file)
                    return json_entities
            except IndexError:
                print(" ! can't remove")


if __name__ == "__main__":
    storage = StorageUtility()
    # storage.update_entity_by_coordinate_value(4, 8, 'Right', False, './simulation_data/robo_vs_dino.json')
    # print(storage.read_json('./simulation_data/robo_vs_dino.json'))



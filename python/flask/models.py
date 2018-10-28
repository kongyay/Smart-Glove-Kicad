import json
from mongoengine import Document, EmbeddedDocument, connect
from mongoengine import StringField, ReferenceField, ListField, URLField, EmbeddedDocumentField

connect('g2g')


class Pose(Document):
    name = StringField(max_length=60, required=True, unique=True)
    pic = URLField(max_length=500)

    def to_json(self):
        jsonObj = {}
        jsonObj["name"] = self.name
        jsonObj["pic"] = self.pic or ""
        return jsonObj


class Movement(Document):
    name = StringField(max_length=60, required=True, unique=True)
    pic = URLField(max_length=500)

    def to_json(self):
        jsonObj = {}
        jsonObj["name"] = self.name
        jsonObj["pic"] = self.pic or ""

        return jsonObj


class Step(EmbeddedDocument):
    name = StringField(max_length=60)
    pose = ReferenceField(Pose, required=True)
    movement = ReferenceField(Movement, required=True)

    def to_json(self):
        jsonObj = {}
        jsonObj["name"] = self.name or ""
        jsonObj["pose"] = self.pose.to_json()
        jsonObj["movement"] = self.movement.to_json()
        return jsonObj


class Gesture(Document):
    name = StringField(max_length=60, required=True, unique=True)
    steps = ListField(EmbeddedDocumentField(Step), required=True)

    def to_json(self):
        jsonObj = {}
        jsonObj["name"] = self.name
        jsonObj["steps"] = []
        for s in self.steps:
            jsonObj["steps"].append(s.to_json())
        return jsonObj

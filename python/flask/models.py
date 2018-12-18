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

class Gesture(Document):
    name = StringField(max_length=60, required=True, unique=True)
    poses = ListField(ReferenceField(Pose), required=True)

    def to_json(self):
        jsonObj = {}
        jsonObj["name"] = self.name
        jsonObj["poses"] = []
        for p in self.poses:
            jsonObj["poses"].append(p.to_json())
        return jsonObj

class Action(Document):
    name = StringField(max_length=60, required=True, unique=True)
    pic = URLField(max_length=500)
    
    def to_json(self):
        jsonObj = {}
        jsonObj["name"] = self.name
        jsonObj["pic"] = self.pic or ""
        return jsonObj

class GestureAction(EmbeddedDocument):
    gesture = ReferenceField(Gesture, required=True)
    action = ReferenceField(Action, required=True)
    args = ListField(StringField(max_length=500))

    def to_json(self):
        jsonObj = {}
        jsonObj["gesture"] = self.gesture.to_json()
        jsonObj["action"] = self.action.to_json()
        jsonObj["args"] = []
        for a in self.args:
            jsonObj["args"].append(a)
        return jsonObj

class Profile(Document):
    name = StringField(max_length=60, required=True, unique=True)
    gestures_actions = ListField(EmbeddedDocumentField(GestureAction), required=True)

    def to_json(self):
        jsonObj = {}
        jsonObj["name"] = self.name
        jsonObj["gestures_actions"] = []
        for ga in self.gestures_actions:
            jsonObj["gestures_actions"].append(ga.to_json())
        return jsonObj

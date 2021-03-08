import uuid

uid = uuid.uuid4()
options = {
    "topic": 'quickstart-events',
    "servers": ["localhost:9092"],
    "groupId": "notification_center_%s" % str(uid)
}

from kafka import KafkaConsumer
import utils.LogMgr as log

logger = log.GetLogger()


def get(options, key, default):
    if options is None or key not in options:
        return default

    return options[key]


def listen(options, subscribe_callback=None):
    topic = get(options, "topic", 'test')
    adr = get(options, "servers", "localhost:9092")
    groupId = get(options, "groupId", "notification_center")

    logger.debug("start listen kafka message queue: topic[%s], servers[%s], groupId[%s]" % (
        topic, adr, groupId))
    cosumer = KafkaConsumer(topic, bootstrap_servers=adr, group_id=groupId)
    if subscribe_callback is not None:
        for msg in cosumer:
            recv = "%s:%d:%d: key=%s value=%s" % (
                msg.topic, msg.partition, msg.offset, msg.key, msg.value)
            logger.debug(recv)
            subscribe_callback(msg.value)

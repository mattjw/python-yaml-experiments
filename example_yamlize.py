from yamlize import Object, Attribute, Sequence

#
# Defaults as constants

DEFAULT_ELASTIC_HOST = "localhost"
DEFAULT_ELASTIC_PORT = 9200
DEFAULT_KAFKA_HOST = "kafka"
DEFAULT_REDIS_HOST = "redis"

#
# Classes as schema

class Node(Object):
    host = Attribute(type=str, default=DEFAULT_ELASTIC_HOST)
    port = Attribute(type=int, default=DEFAULT_ELASTIC_PORT)

class Nodes(Sequence):
    item_type = Node

class Elastic(Object):
    nodes = Attribute(type=Nodes)

class RequiredDefaults(Object):
    x = Attribute(type=str, default="val-x")
    y = Attribute(type=str, default="val-y")

class JobBatch(Object):
    redis_host = Attribute(type=str, default=DEFAULT_REDIS_HOST)

class JobStreaming(Object):
    kafka_broker = Attribute(type=str, default=DEFAULT_KAFKA_HOST)

class ConfigRoot(Object):
    my_int = Attribute(type=int)
    my_float = Attribute(type=float)
    my_str = Attribute(type=str)
    description = Attribute(type=str)

    required_defaults = Attribute(type=RequiredDefaults, default=RequiredDefaults())

    job_batch = Attribute(type=JobBatch, default=None)
    job_streaming = Attribute(type=JobStreaming, default=None)
    
    elastic = Attribute(type=Elastic)

#
# Parsing demo

raw = """
my_int: 3
my_float: 3.5
my_str: hello
job_batch:
  redis_host: hello
elastic:
  nodes:
  - host: localhsot
    port: 9200
  - host: elastic1
    port: 10200
description: >
    multi-line
    description
"""

out = ConfigRoot.load(raw)

print("root:               ", [f"<{f}>" for f in [out.my_int, out.my_float, out.my_str, out.description]])
print("elastic:            ", ".nodes", [(node.host, node.port) for node in out.elastic.nodes])
print("required_defaults:  ", ".x", out.required_defaults.x, "|", ".y", out.required_defaults.y)
print("job_batch:          ", ".redis_host", out.job_batch.redis_host)
print("job_streaming:      ", out.job_streaming)

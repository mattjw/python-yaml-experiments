from yamlize import Object, Attribute, Sequence

#
# Defaults as constants

DEFAULT_ELASTIC_HOST = "localhost"
DEFAULT_ELASTIC_PORT = 9200

#
# Classes as schema

class Node(Object):
    host = Attribute(type=str)
    port = Attribute(type=int)

class Nodes(Sequence):
    item_type = Node

class Elastic(Object):
    nodes = Attribute(type=Nodes)

class JobBatch(Object):
    redis_host = Attribute(type=str)

class JobStreaming(Object):
    kafka_broker = Attribute(type=str)

class ConfigRoot(Object):
    my_int = Attribute(type=int)
    my_float = Attribute(type=float)
    my_str = Attribute(type=str)
    description = Attribute(type=str)

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

print("root", [f"<{f}>" for f in [out.my_int, out.my_float, out.my_str, out.description]])
print("elastic", ".nodes", [(node.host, node.port)for node in out.elastic.nodes])
print("job_batch", ".redis_host", out.job_batch.redis_host)
print("job_streaming", out.job_streaming)

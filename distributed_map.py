import hazelcast
from tqdm import tqdm

ip = '172.20.96.1'

client = hazelcast.HazelcastClient(
    cluster_name="hazelcast-cluster",
    cluster_members = [ip+":5701", ip+":5702", ip+":5703"] )

my_map = client.get_map("my-distributed-map").blocking()
my_map.clear()

for i in tqdm(range(1000)):
    my_map.put("key" + str(i), "value" + str(i))
print("Finished putting 1000 entries")

for i in tqdm(range(1000)):
    value = my_map.get("key" + str(i))
print(f"Finished getting 1000 entries, last value: {value}")

client.shutdown()

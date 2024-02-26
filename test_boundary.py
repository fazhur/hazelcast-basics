import hazelcast
from tqdm import tqdm

def test_boundary():
    ip = '172.20.96.1'
    client = hazelcast.HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members = [ip+":5701"] )
    my_queue = client.get_queue("my-distributed-queue").blocking()
    my_queue.clear()
    for i in range(100):
        print(f'Putting {i} into the queue')
        my_queue.put(i)
    while not my_queue.is_empty():
        print(my_queue.take())
    client.shutdown()

if __name__ == "__main__":
    test_boundary()

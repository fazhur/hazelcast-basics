import hazelcast
import multiprocessing
import time

def write_to_queue():
    ip = '172.20.96.1'
    client = hazelcast.HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members = [ip+":5701"] )
    my_queue = client.get_queue("my-distributed-queue").blocking()
    my_queue.clear()
    for i in range(100):
        responce = my_queue.offer(i)
        while not responce:
            responce = my_queue.offer(i)
        print(f'Inserted value {i}')
    client.shutdown()


def read_from_queue():
    ip = '172.20.96.1'
    client = hazelcast.HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members = [ip+":5701"] )
    my_queue = client.get_queue("my-distributed-queue").blocking()
    uuid = hash(client._CLIENT_ID)
    while not my_queue.is_empty():
        print(f'Extracted value {my_queue.take()} by client {uuid}')
    client.shutdown()

if __name__ == "__main__":
    ip = '172.20.96.1'
    client = hazelcast.HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members = [ip+":5701"] )
    my_queue = client.get_queue("my-distributed-queue").blocking()
    my_queue.clear()
    print(f'Queue cleaned, size: {my_queue.size()}')
    client.shutdown()
    
    clients = []
    cl = multiprocessing.Process(target=write_to_queue)
    cl.start()
    clients.append(cl)
    # time.sleep(1)
    for i in range(2):
        cl = multiprocessing.Process(target=read_from_queue)
        cl.start()
        clients.append(cl)

    for cl in clients:
        cl.join()
    exit()
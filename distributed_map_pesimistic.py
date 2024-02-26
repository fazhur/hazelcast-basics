import hazelcast
import multiprocessing


def run_client():
    ip = '172.20.96.1'

    client = hazelcast.HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members = [ip+":5701", ip+":5702", ip+":5703"] )

    my_map = client.get_map("increment").blocking()
    my_map.put_if_absent("counter", 0)

    for i in range(10000):
        my_map.lock("counter")
        try:
            val = my_map.get("counter")
            val += 1
            my_map.put("counter", val)
        finally:
            my_map.unlock("counter")
    client.shutdown()

if __name__ == "__main__":
    ip = '172.20.96.1'

    master_client = hazelcast.HazelcastClient(
        cluster_name="hazelcast-cluster",
        cluster_members = [ip+":5701", ip+":5702", ip+":5703"] )

    my_map = master_client.get_map("increment").blocking()
    my_map.clear()

    clients = []
    for i in range(3):
        cl = multiprocessing.Process(target=run_client)
        cl.start()
        clients.append(cl)

    for cl in clients:
        cl.join()

    my_map = master_client.get_map("increment").blocking()
    print(f'Final value of counter using pesimistic locking: {my_map.get("counter")}')
    master_client.shutdown()

import time

from blockchain import Blockchain
from genesisblock import GenesisBlock
from multiprocessing import Process
from node import Node


if __name__ == '__main__':
    genesis_block = GenesisBlock()
    genesis_block.show()

    blockchain = Blockchain()
    blockchain.append(genesis_block)

    num_nodes = 3
    nodes = dict()
    processes = []

    # create nodes
    for index in range(num_nodes):
        if index == 0:
            # bootstrap via root node
            node = Node(blockchain=blockchain)
            nodes[node.id] = node.get_settings()
        else:
            node = Node(known_nodes=nodes)

        try:
            process = Process(target=node.run)
            processes.append(process)
            process.start()
            time.sleep(1)
        except Exception as exc:
            print("Error: {}.".format(str(exc)))

    # wait until everybody has finished
    for process in processes:
        process.join()

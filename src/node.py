import json
import math
import random
import requests
import sys
import uuid

from abstractblock import AbstractBlock
from block import Block
from blockchain import Blockchain
from copy import copy
from flask import Flask
from flask import request
from flask import Response
from jsonschema import validate, ValidationError
from multiprocessing import Lock
from transactiondatav1 import TransactionDataV1


class Node:
    def __init__(self, blockchain=None, known_nodes=None, local=True):
        self._node = Flask(__name__)

        if local:
            self._ip="127.0.0.1"
        else:
            json_ip = json.loads(requests.get('http://httpbin.org/ip').text)
            self._ip = json_ip['origin']

        self._port = \
            random.randint(
                10000,
                int(math.pow(2,16)-1)
            )

        self._id = uuid.uuid4().hex

        if blockchain is None:
            self._blockchain = Blockchain()
        else:
            self._blockchain = blockchain
        self._blockchain_lock = Lock()

        if known_nodes is None:
            # <node_id>: { "ip": <ip>, "port": <port> }
            self._known_nodes = dict()
        else:
            self._known_nodes = known_nodes
        self._known_nodes_lock = Lock()

        self._add_endpoints()
        self._startup_sequence()

    #
    # query read-only properties
    #

    @property
    def port(self):
        return self._port

    @property
    def id(self):
        return self._id

    def get_settings(self):
        ret_val = \
            {
              "ip": self._ip,
              "port": self._port
            }
        return ret_val

    #
    # getters and setters
    #

    def get_blockchain(self):
        with self._blockchain_lock:
            return copy(self._blockchain)

    def set_blockchain(self, blockchain):
        if isinstance(blockchain, Blockchain):
            with self._blockchain_lock:
                self._blockchain = blockchain
        else:
            raise Exception(
                "{} Argument provided is of type {} (not of expected type {})."
                .format(self._id, type(blockchain).__name__, type(Blockchain).__name__)
            )

    def append_to_blockchain(self, block):
        if isinstance(block, AbstractBlock):
            with self._blockchain_lock:
                self._blockchain.append(block)
        else:
            raise Exception(
                "{} Argument provided is of type {} (not of expected type {})."
                .format(self._id, type(block).__name__, type(AbstractBlock).__name__)
            )

    def get_known_nodes(self):
        with self._known_nodes_lock:
            return copy(self._known_nodes)

    def add_known_nodes(self, nodes):
        if isinstance(nodes, dict):
            with self._known_nodes_lock:
                self._known_nodes.update(nodes)
        else:
            raise Exception(
                "{} Argument provided is of type {} (not of expected type {})."
                .format(self._id, type(nodes).__name__, type(dict).__name__)
            )

    #
    # REST SERVER
    #

    def run(self):
        print("{} Starting node on port {}.".format(self._id, self._port))

        self._node.run(
            port=self._port,
            threaded=True
        )

    def _add_endpoints(self):
        self._node.add_url_rule(
            rule="/nodes",
            endpoint="_get_nodes",
            view_func=self._get_nodes,
            methods=['GET']
        )

        self._node.add_url_rule(
            rule="/blockchain/length",
            endpoint="_get_blockchain_length",
            view_func=self._get_blockchain_length,
            methods=['GET']
        )

        self._node.add_url_rule(
            rule="/blockchain",
            endpoint="_get_blockchain",
            view_func=self._get_blockchain,
            methods=['GET']
        )

    def _startup_sequence(self):
        self._update_known_nodes()
        node_with_longest_blockchain = self._identify_node_with_longest_blockchain()
        if node_with_longest_blockchain is not None:
            self._update_blockchain(node_with_longest_blockchain)

    #
    # -> queries to other nodes
    #

    def _update_known_nodes(self):
        endpoint = "/nodes"
        with self._known_nodes_lock:
            for key in self._known_nodes.keys():
                response = \
                    requests.get(
                        "http://" + self._known_nodes[key]["ip"] + ":" +
                        str(self._known_nodes[key]["port"]) + endpoint
                    )
                json_response = response.json()

                print(
                    "{} {}->{} ({}): {}"
                    .format(
                        self._id,
                        self._port,
                        self._known_nodes[key]["port"],
                        endpoint,
                        json_response
                    )
                )

                if len(json_response.keys()) != 0:
                    self.add_known_nodes(json_response)

    def _identify_node_with_longest_blockchain(self):
        endpoint = "/blockchain/length"

        longest_blockchain = 0
        longest_blockchain_node = None

        with self._known_nodes_lock:
            for key in self._known_nodes.keys():
                response = \
                    requests.get(
                        "http://" + self._known_nodes[key]["ip"] + ":" +
                        str(self._known_nodes[key]["port"]) + endpoint
                    )
                json_response = response.json()

                print(
                    "{} {}->{} ({}): {}"
                    .format(
                        self._id,
                        self._port,
                        self._known_nodes[key]["port"],
                        endpoint,
                        json_response
                    )
                )

                length = int(json_response["length"])
                if length > longest_blockchain:
                    longest_blockchain = length
                    longest_blockchain_node = key

        return longest_blockchain_node

    def _update_blockchain(self, node_with_longest_blockchain):
        with self._known_nodes_lock:
            node_info = self._known_nodes[node_with_longest_blockchain]

        endpoint = "/blockchain"
        response = \
            requests.get(
                "http://" + node_info["ip"] + ":" +
                str(node_info["port"]) + endpoint
            )
        json_response = response.json()

        print(
            "{} {}->{} ({}): {}"
                .format(
                self._id,
                self._port,
                node_info["port"],
                endpoint,
                json_response
            )
        )

        # TODO Update blockchain
        # TODO validate json schemas
        # TODO keep information about nodes (locally within node)
        # TODO chainbase
        # TODO proof-of-work

    #
    # -> respond to queries from other nodes
    #

    def _get_blockchain_length(self):
        response_code = 200

        with self._blockchain_lock:
            ret_val = { "length": str(self._blockchain.get_length()) }

        return Response(
            json.dumps(ret_val),
            response_code
        )

    def _get_blockchain(self):
        if request.method == 'GET':
            return Response(
                json.dumps(self.get_blockchain().json_dict()),
                200
            )

    def _get_nodes(self):
        response_code = 200

        return Response(
            json.dumps(self.get_known_nodes()),
            response_code
        )

    # def transaction_v1(self):
    #     if request.method == 'POST':
    #         request_data = request.get_json()
    #
    #         self._transaction_v1_schema = \
    #             json.load(
    #                 open("../schema/transactiondatav1.json")
    #             )
    #
    #         try:
    #             validate(request_data, self._transaction_v1_schema)
    #         except ValidationError as ve:
    #             print("Error: {}.".format(str(ve)), file=sys.stderr)
    #             return Response(str(ve), 400)
    #
    #         response_code = 200
    #         response_string = "{} Transaction successfully added to blockchain.".format(self._id)
    #
    #         with self._blockchain_lock:
    #             last_block = self._blockchain.get_last()
    #
    #             if last_block is not None:
    #                 transaction = TransactionDataV1(request_data)
    #
    #                 new_block = \
    #                     Block(
    #                         data=transaction,
    #                         index=last_block.index + 1,
    #                         previous_hash=last_block.hash
    #                     )
    #                 self._blockchain.append(new_block)
    #             else:
    #                 response_code = 500
    #                 response_string = "{} Last block could not be extracted from blockchain.".format(self._id)
    #
    #         return Response(
    #             response_string,
    #             response_code
    #         )


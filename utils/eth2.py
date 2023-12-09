import logging
import requests


class BeaconNode:
    BEACON_SLOT_PER_EPOCH = 0
    BEACON_TIME_PER_SLOT = 0
    EPOCH_PER_TIME_PERIOD = 0
    GENESIS_TIME = None
    STATUSES = ["active", "active_ongoing"]
    api_url = None

    api_version = '/eth/v1/node/version'
    api_genesis = '/eth/v1/beacon/genesis'
    api_headers = '/eth/v1/beacon/headers'
    api_beacon_finalized_slot = '/eth/v1/beacon/headers/finalized'
    # api_get_balances = '/eth/v1/beacon/states/{}/validator_balances?id={}'
    api_get_validator = '/eth/v1/beacon/states/{}/validators/{}'
    api_get_all_validator = '/eth/v1/beacon/states/{}/validators'
    api_node_syncing = '/eth/v1/node/syncing'

    def __init__(self, connection_addr):
        self._connect(connection_addr)

    def query_beacon_node(self, query):
        """

        :param query:
        :return:
        """
        response = requests.get(self.api_url + query)
        if response.status_code < 300:
            return response.json()
        elif response.status_code == 404:
            logging.warning("Data not present on beacon")
            return None
        else:
            logging.error("Can't connect to the beacon node")
            response.raise_for_status()
            return None

    def get_validators(self) -> dict:
        """
        :return: all validators
        """
        query = self.api_get_all_validator.format('finalized')
        return self.query_beacon_node(query)["data"]

    def get_current_slot(self):
        return int(self.query_beacon_node(self.api_headers)["data"][0]["header"]["message"]["slot"])

    def get_withdrawal_balance(self, val_pub_key,epoch):
        """
        :param epoch: slot for which the balance is to be calculated
        :param val_pub_key: validator key for which withdrawal credentials are to be calculated
        :return:
        """
        query = self.api_get_validator.format((int(epoch)*32)-1, val_pub_key)
        validator_param = self.query_beacon_node(query)
        if validator_param is None:
            logging.error("{}: validator not present on eth2 side".format(val_pub_key))
            return None
        return validator_param["data"]["balance"]

    def _connect(self, connection_addr):
        self.api_url = connection_addr
        self.GENESIS_TIME = self.query_beacon_node(self.api_genesis)["data"]["genesis_time"]
        if "Prysm" in self.query_beacon_node(self.api_version)["data"]["version"]:
            logging.info("connected to prysm beacon chain")
        elif "Lighthouse" in self.query_beacon_node(self.api_version)["data"]["version"]:
            logging.info("connected to Lighthouse beacon chain")

    def get_finalized_slot(self):
        return self.query_beacon_node(self.api_beacon_finalized_slot)["data"]["header"]["message"]["slot"]

    def is_node_syncing(self):
        return self.query_beacon_node(self.api_node_syncing)["data"]["is_syncing"]



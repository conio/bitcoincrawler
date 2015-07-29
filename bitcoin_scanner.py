__author__ = 'mirko'

class BitcoinScanner(object):
    def __init__(self, blocks_generator, node_backend):
        self.blocks_generator = blocks_generator
        self.node_backend = node_backend
        self.blocks_observers = []
        self.transactions_observers = []
        self.mempool_transactions_observers = []
        self.inputs_observers = []
        self.outputs_observers = []
        self.mempool_inputs_observers = []
        self.mempool_outputs_observers = []

    def __notify_block(self, cur_block):
        for n in self.blocks_observers:
            n.on_block(cur_block)

    def __notify_transaction_blockchain_or_mempool(self, cur_tx, tx_observers, in_observers, out_observers):
        for n in tx_observers:
            n.on_transaction(cur_tx)

        if len(in_observers) > 0:
            for vin in cur_tx.vin:
                for i_n in in_observers:
                    i_n.on_input(vin)

        if len(out_observers) > 0:
            for vout in cur_tx.vout:
                for o_n in out_observers:
                    o_n.on_output(vout)

    def notify_transaction(self, cur_tx):
        self.__notify_transaction_blockchain_or_mempool(
            cur_tx, self.transactions_observers,
            self.inputs_observers, self.outputs_observers
        )

    def notify_mempool_transaction(self, cur_tx):
        self.__notify_transaction_blockchain_or_mempool(
            cur_tx, self.mempool_transactions_observers,
            self.mempool_inputs_observers, self.mempool_outputs_observers
        )
    def scan(self):
        notify_tx = \
            len(self.transactions_observers) > 0 \
            or len(self.inputs_observers) > 0 \
            or len(self.outputs_observers) > 0

        notify_mempool_tx = \
            len(self.mempool_transactions_observers) > 0 \
            or len(self.mempool_inputs_observers) > 0 \
            or len(self.mempool_outputs_observers) > 0

        notify_block = len(self.blocks_observers) > 0 or notify_tx

        if notify_block:
            for cur_block in self.blocks_generator:
                self.__notify_block(cur_block)
                if notify_tx:
                    for tx in cur_block.tx:
                        self.notify_transaction(tx)

        if notify_mempool_tx:
            for cur_transaction in self.node_backend.get_mempool_transactions():
                self.notify_mempool_transaction(cur_transaction)

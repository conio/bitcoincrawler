__author__ = 'guido'
from components.model import Block, Transaction, Vin, Vout

class BTCDBlock(Block):
    def __init__(self, json_obj, node_backend):
        self.json_obj = json_obj
        self.node_backend = node_backend
        self.genesis_block_tx = '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b'

    @property
    def hash(self):
        return self.json_obj.get('hash')

    @property
    def confirmations(self):
        return self.json_obj.get('confirmations')

    @property
    def size(self):
        return self.json_obj.get('size')

    @property
    def height(self):
        return self.json_obj.get('height')

    @property
    def version(self):
        return self.json_obj.get('version')

    @property
    def merkleroot(self):
        return self.json_obj.get('merkleroot')

    @property
    def tx(self):
        return (BTCDTransaction(self.node_backend.get_transaction(tx)) for tx in self.json_obj.get('tx') if \
                tx != self.genesis_block_tx)

    @property
    def time(self):
        return self.json_obj.get('time')

    @property
    def coinbase(self):
        txs = self.json_obj.get('tx')
        if txs:
            return BTCDTransaction(txs[0])
        return None

    @property
    def nonce(self):
        return self.json_obj.get('nonce')

    @property
    def bits(self):
        return self.json_obj.get('bits')

    @property
    def difficulty(self):
        return self.json_obj.get('difficulty')

    @property
    def chainwork(self):
        return self.json_obj.get('chainwork')

    @property
    def previousblockhash(self):
        return self.json_obj.get('previousblockhash')

    @property
    def nextblockhash(self):
        return self.json_obj.get('nextblockhash')

class BTCDTransaction(Transaction):
    def __init__(self, json_obj):
        self.json_obj = json_obj

    @property
    def txid(self):
        return self.json_obj.get('txid')

    @property
    def version(self):
        return self.json_obj.get('version')

    @property
    def locktime(self):
        return self.json_obj.get('locktime')

    @property
    def vin(self):
        print(self.json_obj)
        return (BTCDVout(vout) for vout in self.json_obj.get('vin'))

    @property
    def vout(self):
        return (BTCDVout(vout) for vout in self.json_obj.get('vout'))

    @property
    def txid(self):
        return self.json_obj.get('txid')

    @property
    def txid(self):
        return self.json_obj.get('txid')

class BTCDVin(Vin):
    def __init__(self, json_obj):
        self.json_obj = json_obj

    @property
    def scriptSig(self):
        j = self.json_obj
        class ScriptSig:
            @property
            def hex(self):
                try: return j.get('scriptSig').get('hex')
                except AttributeError: return None

            @property
            def asm(self):
                try: return j.get('scriptSig').get('asm')
                except AttributeError: return None

        return ScriptSig()

    @property
    def sequence(self):
        return self.json_obj.get('sequence')

    @property
    def vout(self):
        return self.json_obj.get('vout')

    @property
    def txid(self):
        return self.json_obj.get('txid')

    @property
    def coinbase(self):
        return self.json_obj.get('coinbase')


class BTCDVout(Vout):
    def __init__(self, json_obj):
        self.json_obj = json_obj
    @property
    def value(self):
        return self.json_obj.get('value')

    @property
    def n(self):
        return self.json_obj.get('n')

    @property
    def scriptPubKey(self):
        j = self.json_obj
        class ScriptPubKey:
            @property
            def asm(self):
                try: return j.get('scriptPubKey').get('asm')
                except AttributeError: return None

            @property
            def hex(self):
                try: return j.get('scriptPubKey').get('hex')
                except AttributeError: return None

            @property
            def reqSigs(self):
                try: return j.get('scriptPubKey').get('reqSigs')
                except AttributeError: return None

            @property
            def type(self):
                try: return j.get('scriptPubKey').get('type')
                except AttributeError: return None

            @property
            def addresses(self):
                try: return j.get('scriptPubKey').get('addresses')
                except AttributeError: return None

        return ScriptPubKey()
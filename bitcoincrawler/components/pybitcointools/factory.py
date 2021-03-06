from bitcoincrawler.components.bitcoind.factory import BitcoindFactory
from bitcoincrawler.components.tools import chain
from bitcoincrawler.components.pybitcointools.model import PyBitcoinToolsTransaction
import asyncio

class PyBitcoinToolsFactory(BitcoindFactory):
    """
    Extension of bitcoind component, use local parser instead of decoderawtransaction.
    Looks faster and surely consume less network resources, but it's _HIGHLY EXPERIMENTAL__.
    """
    def __init__(self, bitcoind_cli, async=False):
        super(PyBitcoinToolsFactory, self).__init__(bitcoind_cli, async=async)

    def _get_transaction(self, txid, parent_block=None):
        meta = {'parent_block': parent_block}
        """
        Since we already have the txid information
        """
        if self.async:
            return chain(txid,
                         lambda txid: self.btcd.get_raw_transaction(txid, async=True),
                         asyncio.coroutine(lambda rawtx: PyBitcoinToolsTransaction(rawtx.get('result'),
                                                                                   txid,
                                                                                   network=self.network,
                                                                                   meta=meta)))
        else:
            return PyBitcoinToolsTransaction(self.btcd.get_raw_transaction(txid).get('result'),
                                             txid,
                                             meta=meta)
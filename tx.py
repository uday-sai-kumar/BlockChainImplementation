from script import Script


class Tx:
    def __init__(self, version, tx_ins, tx_outs,
                 locktime, _timestamp, tx_hash=None):
        self.tx_hash = tx_hash
        self.version = version
        self._timestamp = _timestamp
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        # self._hash_prevouts = None
        # self._hash_sequence = None
        # self._hash_outputs = None

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return '\n tx: version: {}\n tx_ins:\n{} tx_outs:\n{} locktime: {}\n'.format(
            self.version,
            tx_ins,
            tx_outs,
            self.locktime,
        )


class TxIn:

    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return ' previous_trasaction:{}\n previous_index:{}\n script_signature: {}\n'.format(
            self.prev_tx,
            self.prev_index,
            self.script_sig
        )


class TxOut:

    def __init__(self, amount, address, script_pubkey):
        self.amount = amount
        self.address = address
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return ' amount:{} BTC \n address: {}\n script_publickey:{}\n'.format(self.amount, self.address, self.script_pubkey)

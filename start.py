from Account import MyAccount
from ecc import PrivateKey, PrivateKey, Signature
from helper import hash256, hash160, encode_base58
from helper import merkle_root, merkle_parent_level, merkle_parent
from block import Block
from datetime import datetime
from tx import Tx, TxIn, TxOut
import random
seed = 'welcome to blockchain'  # seed used for generating the private keys
private_keys = []
public_keys = []
bitcoin_addresses = []
my_accounts = {}
current_transactions = []
current_transactions_hashes = []
# s256fields = []
for i in range(10):
    private_keys.append(hash256((seed+str(i)).encode('utf-8')).hex())
print('Private Keys')
for i in range(10):

    print('[{}] {}'.format(i, private_keys[i]))


# generating public keys from private keys
for i in range(10):
    key1 = PrivateKey(int('0x'+private_keys[i], 16))
    # s256fields.append(key1.point)
    public_keys.append(key1)
    _hash = hash160(
        (str(key1.point.x)+str(key1.point.y)).encode('utf-8')).hex()
    _hash = '00'+_hash
    # print(_hash)
    bitcoin_addresses.append(encode_base58(bytes.fromhex(_hash)))

    # account1=MyAccount()
    # account2=MyAccount()
    # account3=MyAccount()


# adding eveything into accounts
for i in range(10):
    account1 = MyAccount(
        private_keys[i], public_keys[i], bitcoin_addresses[i], [], 0)
    my_accounts[bitcoin_addresses[i]] = account1
    print(bitcoin_addresses[i])

# print("Enter amount to send")
# amount=input()


# creating the coin base transaction


blockchain = []
_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
# script__public__key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
# bitcoin_addresses[0])

t_input = TxIn(prev_tx='COINBASE (Newly Generated Coins)', prev_index=0,
               script_sig=None, sequence=0xffffffff)
script_public_key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
    bitcoin_addresses[0])
t_out = TxOut(50, bitcoin_addresses[0], script_public_key)
t__input = [t_input]
t__out = [t_out]
genesis_transaction = Tx(1, t__input, t__out, 0,
                         datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

transaction_id = hash256(repr(genesis_transaction).encode('utf-8')).hex()
# print(transaction_id)
genesis_transaction.tx_hash = transaction_id

genesis_block = Block(version=1, prev_block=str(0x00000000000000000000000000000000), merkle_root=None,
                      timestamp=_time, bits=None, nonce=None, tx_hashes=[transaction_id], tx_objects=[genesis_transaction])
merkle__root = merkle_root([transaction_id])
genesis_block.merkle_root = merkle__root
my_accounts[genesis_transaction.tx_outs[0].address].utxo = [
    genesis_transaction.tx_outs[0]]
genesis_block.block_hash = str(genesis_block.hash())  # block hash
blockchain.append(genesis_block)  # adding to the block chain


def _create_coinbase_transaction(_miner):
    _time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    t_input = TxIn(prev_tx='COINBASE (Newly Generated Coins)', prev_index=0,
                   script_sig=None, sequence=0xffffffff)
    script_public_key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
        bitcoin_addresses[_miner])
    t_out = TxOut(50, bitcoin_addresses[_miner], script_public_key)
    t__input = [t_input]
    t__out = [t_out]
    coinbase_transaction = Tx(1, t__input, t__out, 0,
                              datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    transaction_id = hash256(repr(coinbase_transaction).encode('utf-8')).hex()
    # print(transaction_id)
    coinbase_transaction.tx_hash = transaction_id
    my_accounts[bitcoin_addresses[_miner]].utxo.append(
        coinbase_transaction.tx_outs[0])
    return coinbase_transaction


# verifying the transaction using elliptic curve cryptography

def _verify_transactions():
    start = 0
    for __x in current_transactions:
        my_hash = current_transactions_hashes[start]
        start = start+1
        for __p in __x.tx_ins:
            signature = Signature.parse(__p.script_sig)

            if (my_accounts[__p.prev_tx[0].address].public.point.verify(
                    int('0x'+my_hash, 16), signature)) == False:  # removing the transactions those are failed
                current_transactions.remove(__x)

    # for tran_obs in current_transactions:


def _create_block(tx_hashes, my_tx_objects):
    _miner = random.randint(0, 9)
    if (len(my_tx_objects) == 0):
        return
    print("mining")
    print('miner is :')
    print(_miner)
    prev_block = blockchain[len(blockchain)-1].block_hash

    _objects = my_tx_objects.copy()
    _block = Block(version=1, prev_block=prev_block, merkle_root=merkle_root(tx_hashes),
                   timestamp=_time, bits=0, nonce=0, tx_hashes=tx_hashes, tx_objects=_objects)

    my_hash = _block.hash()
    _block.block_hash = str(my_hash)
    for __x in my_tx_objects:
        amount = 0
        for __input in __x.tx_ins:
            for __prev_tx in __input.prev_tx:
                amount += __prev_tx.amount

        for __y in __x.tx_outs:
            my_accounts[__y.address].utxo.append(
                __y)
            amount -= __y.amount

        script_public_key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
            __x.tx_ins[0].prev_tx[0].address)
        my_accounts[__x.tx_ins[0].prev_tx[0].address].utxo.append(
            TxOut(amount, __x.tx_ins[0].prev_tx[0].address, script_public_key))

    current_transactions_hashes.clear()
    current_transactions.clear()
    _block.tx_objects.append(_create_coinbase_transaction(_miner))
    blockchain.append(_block)


# print(my_accounts[bitcoin_addresses[0]]._balance())


# creating the user transaction
def create_and_send(_a, _b, _amount):
    if my_accounts[bitcoin_addresses[_a]]._balance() < _amount:
        print('failed to create')
        return
    else:
        print('creating')
        _utxo = my_accounts[bitcoin_addresses[_a]].utxo
        picked_utxo = []
        my_amount = 0
        for x in _utxo:
            my_amount += x.amount
            picked_utxo.append(x)
            _utxo.remove(x)
            if my_amount >= _amount:
                break

        my_accounts[bitcoin_addresses[_a]].utxo = _utxo
        script_public_key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
            bitcoin_addresses[_b])
        # script__public__key = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'.format(
        #     bitcoin_addresses[_a])

        t_input = []
        t_out = []
        for _x in picked_utxo:
            t_input.append(TxIn(prev_tx=picked_utxo, prev_index=0,
                           script_sig=None, sequence=0xffffffff))

        t_out.append(TxOut(_amount, bitcoin_addresses[_b], script_public_key))
        t__input = t_input
        t__out = t_out
        my_transaction = Tx(1, t__input, t__out, 0,
                            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

        transaction_id = hash256(
            repr(my_transaction).encode('utf-8')).hex()
        for __input in my_transaction.tx_ins:
            __input.script_sig = public_keys[_a].sign(
                int('0x'+transaction_id, 16)).der()

        current_transactions_hashes.append(transaction_id)
        current_transactions.append(my_transaction)

# verify the transactions and creating the block


def start__():
    _verify_transactions()
    _create_block(current_transactions_hashes, current_transactions)


create_and_send(0, 1, 10)

start__()

create_and_send(0, 3, 20)
start__()

create_and_send(0, 3, 1)
start__()

create_and_send(0, 7, 2)
start__()

create_and_send(0, 6, 2)
start__()

create_and_send(0, 5, 2)
start__()
create_and_send(0, 8, 2)
start__()

create_and_send(0, 3, 2)
start__()

create_and_send(0, 9, 2)
start__()

# print(my_accounts[bitcoin_addresses[1]]._balance())
# print(my_accounts[bitcoin_addresses[0]]._balance())
# print(my_accounts[bitcoin_addresses[3]]._balance())

for i in range(10):
    print(my_accounts[bitcoin_addresses[i]]._balance())

for i in range(len(blockchain)):
    print('block:{}\n'.format(i))
    print(blockchain[i])

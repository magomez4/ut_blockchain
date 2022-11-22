#!/usr/bin/env python3

import json, os, sys

sys.path.append(os.path.dirname(__file__))

from copy import deepcopy
from lib.hash     import hash160
from lib.sign     import sign_tx
from lib.encoder  import encode_tx, encode_script
from lib.helper   import hash_script, get_txid
from lib.rpc      import RpcSocket
from lib.helper import *

#setting up alice wallet RPC socket
fee = 1000
Alicerpc = RpcSocket({'wallet': 'AliceWallet'}) #this gives me an RPC socket associated to the AlliceWallet in my bitcoin core
assert Alicerpc.check()

#setting up bob wallet RPC socket
fee = 1000
Bobrpc = RpcSocket({'wallet': 'BobWallet'}) #this gives me an RPC socket associated to the BobWallet in my bitcoin core
assert Bobrpc.check()

## Get a utxo for Alice.
alice_utxo = Alicerpc.get_utxo(0)

## Get a change address for Alice.
alice_change_txout = Alicerpc.get_recv(fmt='base58')
alice_pubkey_hash  = decode_address(alice_change_txout['address'])

## Get a payment address for Bob.
bob_payment_txout = Bobrpc.get_recv(fmt='base58')
bob_pubkey_hash   = decode_address(bob_payment_txout['address'])

## Calculate our output amounts.
fee = 1000
bob_recv_value = alice_utxo['value'] // 2 #can i change for x ammt?? i think yes, as long as I stay within the utxo ammt
alice_change_value = alice_utxo['value'] // 2 - fee

## The spending transaction.
atob_tx = {
    'version': 1,
    'vin': [{
        # We are unlocking the utxo from Alice.
        'txid': alice_utxo['txid'],
        'vout': alice_utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [
        {
            'value': bob_recv_value,
            'script_pubkey': ['OP_DUP', 'OP_HASH160', bob_pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
        },
        {
            'value': alice_change_value,
            'script_pubkey': ['OP_DUP', 'OP_HASH160', alice_pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
        }
    ],
    'locktime': 0
}

## The redeem script is a basic Pay-to-Pubkey-Hash template.
redeem_script = f"76a914{alice_utxo['pubkey_hash']}88ac"

## We are signing Alice's UTXO using BIP143 standard.
alice_signature = sign_tx(
    atob_tx,                # The transaction.
    0,                      # The input being signed.
    alice_utxo['value'],    # The value of the utxo being spent.
    redeem_script,          # The redeem script to unlock the utxo. 
    alice_utxo['priv_key']  # The private key to the utxo pubkey hash.
)


## Include the arguments needed to unlock the redeem script.
atob_tx['vin'][0]['witness'] = [ alice_signature, alice_utxo['pub_key'] ]

callResult = Alicerpc.call('sendrawtransaction', encode_tx(atob_tx)) #send encoded transaction to the network
print(callResult)

# print(atob_tx)

# print(alice_utxo) 
# print(alice_utxo['value']) 
# print(bob_recv_value) 
# print(alice_change_value)
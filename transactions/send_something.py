#!/usr/bin/env python3

import json, os, sys

sys.path.append(os.path.dirname(__file__))

from copy import deepcopy
from lib.hash     import hash160
from lib.sign     import sign_tx
from lib.encoder  import encode_tx, encode_script
from lib.helper   import hash_script, get_txid
from lib.rpc      import RpcSocket

# print ('helloworld!')

# I need to create two rpc sockets to make rpc calls on 2 wallets
# build a transaction
# broadcast it into the net
# go into regtest and generate some blocks so that it gets out of my mempool

from web3 import Web3
from loguru import logger
from web3.middleware import geth_poa_middleware
from client import Client
import random
import time
import json
import datetime

RPC = "https://rpc.katla.taiko.xyz"

WEB3 = Web3(Web3.HTTPProvider(RPC))
WEB3.middleware_onion.inject(geth_poa_middleware, layer=0)

def get_uni_abi():
    with open('abi_uni.json', 'r') as file:
        return json.load(file)

def get_random_word():
    with open('words.txt', 'r') as file:
        return random.choice([line.strip() for line in file.readlines()]) + "crypto"
    
def get_wallets():
    with open('wallets.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_eip1559_gas(web3):
    latest_block = web3.eth.get_block('latest')
    max_fee_priotiry_gas = web3.eth.max_priority_fee
    max_fee_per_gas = int(latest_block['baseFeePerGas'] * 1.125) + max_fee_priotiry_gas
    return max_fee_priotiry_gas, max_fee_per_gas

def get_inputs(amount, token):
    contrats = {
        'usdc': [
            "0011e559da84dde3f841e22dc33f3adbf184d84a000bb8ae2c46ddb314b9ba74",
            "3c6dee4878f151881333d9000000000000000000000000000000000000000000"
        ],
        'horse': [
            "0011e559da84dde3f841e22dc33f3adbf184d84a0001f4d69d3e64d71844bbdd",
            "a51cd7f23ed3631e9fac49000000000000000000000000000000000000000000"
        ]
    }
    hex1 = WEB3.to_hex(2)
    hex2 = WEB3.to_hex(WEB3.to_wei(amount, 'ether'))
    bytes1 = hex1[2:].zfill(64)
    bytes2 = hex2[2:].zfill(64)
    first_argument = "0x" + bytes1 + bytes2

    hex1 = WEB3.to_hex(1)
    hex2 = WEB3.to_hex(WEB3.to_wei(amount, 'ether'))
    hex3 = WEB3.to_hex(825053000)
    hex4 = WEB3.to_hex(160)
    hex5 = WEB3.to_hex(0)
    hex6 = WEB3.to_hex(43)
    hex7 = contrats.get(token)[0]
    hex8 = contrats.get(token)[1]
    second_argument = "0x" + hex1[2:].zfill(64) + hex2[2:].zfill(64) + hex3[2:].zfill(64) + hex4[2:].zfill(64) + hex5[2:].zfill(64) + hex6[2:].zfill(64) + hex7 + hex8
    return first_argument, second_argument

def swap_eth_to_usdc(key):
    logger.info("Свап eth to usdc")
    abi = get_uni_abi()
    amount = round(random.uniform(0.0001, 0.001), 6)
    client = Client(WEB3, key)
    contract = client.web3.eth.contract(address="0xD2C3cbB943FEd0Cfc8389b14a3f6df518fD46346", abi=abi)
    max_fee_priotiry_gas, max_fee_per_gas = get_eip1559_gas(client.web3)
    try:
        inputs = get_inputs(amount, 'usdc')
        tx = contract.functions.execute(
            WEB3.to_bytes(hexstr=WEB3.to_hex(2816)),
            inputs,
            int(datetime.datetime.now().timestamp()) + 180
            ).build_transaction(
                {
                    'nonce': client.web3.eth.get_transaction_count(client.address),
                    'gas': 200000,
                    'value': client.web3.to_wei(amount, 'ether'),
                    'maxPriorityFeePerGas': max_fee_priotiry_gas,
                    'maxFeePerGas': max_fee_per_gas,
                }
            )
        signed_txn = client.web3.eth.account.sign_transaction(tx, client.private_key)
        txn_hash = client.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Транзакция отправлена. Хэш: {txn_hash.hex()}")
        receipt = client.web3.eth.wait_for_transaction_receipt(txn_hash)
        if (receipt['status'] == 1):
            logger.success(f"Транзакция прошла успешно!")
        else:
            logger.error(f"Ошибка. Статус: {receipt['status']}")
    except Exception as e:
        logger.error(f"Ошибка {e}")

def wrap_eth(key):
    logger.info("Врап eth")
    amount = round(random.uniform(0.001, 0.009), 6)
    client = Client(WEB3, key)
    max_fee_priotiry_gas, max_fee_per_gas = get_eip1559_gas(client.web3)
    try:
        tx = {
            'chainId': 167008,
            'to': WEB3.to_checksum_address("0x0011E559da84dde3f841e22dc33F3adbF184D84A"),
            'value': WEB3.to_wei(amount, 'ether'),
            'nonce': WEB3.eth.get_transaction_count(client.address),
            'data': '0xd0e30db0',
            'maxPriorityFeePerGas': max_fee_priotiry_gas,
            'maxFeePerGas': max_fee_per_gas,
            'gas': 55000
        }
        signed_txn = client.web3.eth.account.sign_transaction(tx, client.private_key)
        txn_hash = client.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Транзакция отправлена. Хэш: {txn_hash.hex()}")
        receipt = client.web3.eth.wait_for_transaction_receipt(txn_hash)
        if (receipt['status'] == 1):
            logger.success(f"Транзакция прошла успешно!")
        else:
            logger.error(f"Ошибка. Статус: {receipt['status']}")
    except Exception as e:
        logger.error(f"Ошибка {e}")

def swap_eth_to_horse(key):
    logger.info("Свап eth to horse")
    abi = get_uni_abi()
    amount = round(random.uniform(0.0001, 0.001), 6)
    client = Client(WEB3, key)
    contract = client.web3.eth.contract(address="0xD2C3cbB943FEd0Cfc8389b14a3f6df518fD46346", abi=abi)
    max_fee_priotiry_gas, max_fee_per_gas = get_eip1559_gas(client.web3)
    try:
        inputs = get_inputs(amount, 'horse')
        tx = contract.functions.execute(
            WEB3.to_bytes(hexstr=WEB3.to_hex(2816)),
            inputs,
            int(datetime.datetime.now().timestamp()) + 180
            ).build_transaction(
                {
                    'nonce': client.web3.eth.get_transaction_count(client.address),
                    'gas': 200000,
                    'value': client.web3.to_wei(amount, 'ether'),
                    'maxPriorityFeePerGas': max_fee_priotiry_gas,
                    'maxFeePerGas': max_fee_per_gas,
                }
            )
        signed_txn = client.web3.eth.account.sign_transaction(tx, client.private_key)
        txn_hash = client.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Транзакция отправлена. Хэш: {txn_hash.hex()}")
        receipt = client.web3.eth.wait_for_transaction_receipt(txn_hash)
        if (receipt['status'] == 1):
            logger.success(f"Транзакция прошла успешно!")
        else:
            logger.error(f"Ошибка. Статус: {receipt['status']}")
    except Exception as e:
        logger.error(f"Ошибка {e}")

def mint_crypto_domain(key):
    logger.info("Минт домена")
    word = get_random_word()
    client = Client(WEB3, key)
    max_fee_priotiry_gas, max_fee_per_gas = get_eip1559_gas(client.web3)
    data = (
        "0x286fbb9700000000000000000000000000000000000000000000000000000000000000c0"
        f"000000000000000000000000{client.address[2:]}"
        "0000000000000000000000000000000000000000000000000000000001e13380"
        "000000000000000000000000e629cc2ca21ae1945dd3e64051627a2dde78b1fc"
        f"000000000000000000000000{client.address[2:]}"
        "0000000000000000000000000000000000000000000000000000000000000000"
        f"{WEB3.to_hex(len(word))[2:].zfill(64)}"
        f"{WEB3.to_hex(text=word)[2:].ljust(64, '0')}"
    )
    try:
        tx = {
            'chainId': 167008,
            'to': WEB3.to_checksum_address("0xE02D9f7a4c98B707de05AC9dC1Cd8b9c13465Bb7"),
            'value': WEB3.to_wei(0.00047304, 'ether'),
            'nonce': WEB3.eth.get_transaction_count(client.address),
            'data': data,
            'maxPriorityFeePerGas': max_fee_priotiry_gas,
            'maxFeePerGas': max_fee_per_gas,
            'gas': 580000
        }
        signed_txn = client.web3.eth.account.sign_transaction(tx, client.private_key)
        txn_hash = client.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f"Транзакция отправлена. Хэш: {txn_hash.hex()}")
        receipt = client.web3.eth.wait_for_transaction_receipt(txn_hash)
        if (receipt['status'] == 1):
            logger.success(f"Транзакция прошла успешно! Минт домена {word} успешен!")
        else:
            logger.error(f"Ошибка. Статус: {receipt['status']}")
    except Exception as e:
        logger.error(f"Ошибка {e}")
    
def random_tasks(min, max):
    tasks = [swap_eth_to_usdc, swap_eth_to_horse, wrap_eth, mint_crypto_domain]
    wallets = get_wallets()
    for num, wallet in enumerate(wallets, start=1):
        logger.info(f"{num}/{len(wallets)}. {WEB3.eth.account.from_key(wallet).address} ")
        amount = random.randrange(min, max)
        for task in random.choices(tasks, k=amount):
            task(wallet)
            sec = random.randint(10, 20)
            logger.info(f"Сплю между следующей транзакцией {sec}")
            time.sleep(sec)
        sec = random.randint(30, 120)
        logger.info(f"Сплю между следующим кошельком {sec}")
        time.sleep(sec)
    logger.success("Скрипт завершил свою работу")

def intro():
    business_card = """
    ╔════════════════════════════════════════╗
    ║        Createad by v1aas               ║
    ║                                        ║
    ║        https://t.me/v1aas              ║
    ║        https://github.com/v1aas        ║
    ║                                        ║
    ╚════════════════════════════════════════╝
    """
    print(business_card)
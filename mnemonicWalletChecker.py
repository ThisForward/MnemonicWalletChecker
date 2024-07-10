import requests
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# BIP39 wordlist
mnemonic = Mnemonic("english")

def generate_mnemonic():
    # Generate a random 12-word mnemonic
    mnemonic_phrase = mnemonic.generate(128)
    return mnemonic_phrase

def is_valid_mnemonic(mnemonic_phrase):
    return mnemonic.check(mnemonic_phrase)

def generate_addresses(mnemonic_phrase):
    # Generate seed from mnemonic
    seed_bytes = Bip39SeedGenerator(mnemonic_phrase).Generate()
    
    # Bitcoin address
    bip44_mst_ctx_btc = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip44_acc_ctx_btc = bip44_mst_ctx_btc.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
    btc_address = bip44_acc_ctx_btc.AddressIndex(0).PublicKey().ToAddress()
    
    # Ethereum address
    bip44_mst_ctx_eth = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    bip44_acc_ctx_eth = bip44_mst_ctx_eth.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
    eth_address = bip44_acc_ctx_eth.AddressIndex(0).PublicKey().ToAddress()
    
    return btc_address, eth_address

def get_btc_balance(address):
    try:
        response = requests.get(f'https://blockchain.info/q/addressbalance/{address}')
        if response.status_code == 200:
            balance_satoshi = int(response.text)
            balance_btc = balance_satoshi / 100000000  # Convert satoshi to BTC
            return balance_btc
        else:
            return 0
    except Exception as e:
        print(f"Error fetching BTC balance: {e}")
        return 0

def get_eth_balance(address):
    api_key = 'APIKEY(ETHER SCAN)'  # Replace with your actual API key
    try:
        response = requests.get(f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}')
        if response.status_code == 200:
            balance_wei = int(response.json().get('result', 0))
            balance_eth = balance_wei / 1000000000000000000  # Convert wei to ETH
            return balance_eth
        else:
            return 0
    except Exception as e:
        print(f"Error fetching ETH balance: {e}")
        return 0

def main():
    found_wallets = []
    while True:
        mnemonic_phrase = generate_mnemonic()
        print(f'Trying mnemonic: {mnemonic_phrase}')
        
        if is_valid_mnemonic(mnemonic_phrase):
            btc_address, eth_address = generate_addresses(mnemonic_phrase)
           # print(f'Generated Bitcoin Address: {btc_address}')
           # print(f'Generated Ethereum Address: {eth_address}')
            
            # Check balances
            btc_balance = get_btc_balance(btc_address)
            eth_balance = get_eth_balance(eth_address)
            
            print(f'BTC Balance: {btc_balance}')
            print(f'ETH Balance: {eth_balance}')
            
            if btc_balance > 0.000001 or eth_balance > 0.000001:
                print(f'Found valid mnemonic with balance: \033[92m{mnemonic_phrase}\033[0m')
                break

if __name__ == '__main__':
    main()

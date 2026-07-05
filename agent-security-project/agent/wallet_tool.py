"""
wallet_tool.py

Minimal wallet interface for the agent to call as a TOOL.
Talks to an Ethereum TESTNET (Sepolia) via a public RPC.

SAFETY:
- Only ever load a TESTNET private key here, funded with worthless testnet ETH
  from a faucet. NEVER put a real/mainnet private key in this project.
- Keep the key in a local .env file (see .env.example) that you do NOT commit
  or share, including with me — I never need to see it. I only need to see
  the *logs/results* of what the agent did.
"""

import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Public Sepolia testnet RPC (no key needed for reads; feel free to swap
# for your own Infura/Alchemy Sepolia endpoint for reliability).
RPC_URL = os.getenv("SEPOLIA_RPC_URL", "https://rpc.sepolia.org")
PRIVATE_KEY = os.getenv("TESTNET_PRIVATE_KEY")  # testnet key only

w3 = Web3(Web3.HTTPProvider(RPC_URL))


def get_agent_address() -> str:
    if not PRIVATE_KEY:
        raise RuntimeError("Set TESTNET_PRIVATE_KEY in your .env (testnet key only).")
    acct = w3.eth.account.from_key(PRIVATE_KEY)
    return acct.address


def get_balance_eth(address: str | None = None) -> float:
    address = address or get_agent_address()
    balance_wei = w3.eth.get_balance(Web3.to_checksum_address(address))
    return w3.from_wei(balance_wei, "ether")


def send_transaction(to_address: str, amount_eth: float) -> dict:
    """
    THE SENSITIVE TOOL. This is the action an attacker wants to hijack.

    In a real agent, this would be gated behind human confirmation,
    an allowlist, or a spending policy. In this baseline/vulnerable
    version, it is NOT — that's the point of the exercise.
    """
    if not PRIVATE_KEY:
        raise RuntimeError("Set TESTNET_PRIVATE_KEY in your .env (testnet key only).")

    acct = w3.eth.account.from_key(PRIVATE_KEY)
    to_address = Web3.to_checksum_address(to_address)

    tx = {
        "from": acct.address,
        "to": to_address,
        "value": w3.to_wei(amount_eth, "ether"),
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    }

    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

    return {
        "status": "sent",
        "tx_hash": tx_hash.hex(),
        "to": to_address,
        "amount_eth": amount_eth,
        "explorer_url": f"https://sepolia.etherscan.io/tx/{tx_hash.hex()}",
    }

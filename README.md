# Agentic Wallet Prompt Injection: A Minimal Case Study

A minimal AI agent (Gemini 2.5 Flash, tool-calling) with two tools:

- `read_source`:- reads external text content (a stand-in for a webpage, doc, or token metadata the agent is asked to summarize)
- `send_transaction`:- signs and sends testnet ETH from the agent's own wallet

**The question:**-if an agent has standing permission to move funds, can content it merely *reads* not content the user typed hijack it into calling that tool without the user asking?

**The result:** *Yes*. Across 3 runs of the same injected document, the agent executed an unauthorized transfer in 2. Both are confirmed on-chain:

- [https://sepolia.etherscan.io/tx/9a53df9a175235bb265f2d5fb6209e354e7335058f3e40b09e160a17384ba3af]
- [https://sepolia.etherscan.io/tx/4c9d15f20ad7fb9d5c214b873eb0ea4afe7745d1a981c1cd5f7a826efe2a2221]

A control document,identical except for the injected instruction never triggered a transfer.

*Injected run*
![injected run screenshot](<Screenshots/Screenshot from 2026-07-04 15-45-37.png>)
*Etherscan confirmation*
![etherscan confirmation](<Screenshots/Screenshot from 2026-07-04 16-12-09.png>)
This isn't hypothetical.In May 2026, the same underlying attack using instructions hidden in untrusted text was used to get an X-linked AI agent (Grok, wired to the Bankr trading bot) to authorize a $150K+ unauthorized token transfer. This project reproduces the same failure mode on a controlled testnet, with fewer moving parts, so the mechanism is easier to see clearly.

Full writeup, threat model, severity analysis, and mitigations: **[[link to full report](https://aqfatma.hashnode.dev/agentic-wallet-prompt-injection-a-minimal-case-study)]**

## Setup

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env`
3. Get a Gemini API key (You can use any LLM's API Key): https://aistudio.google.com/apikey
4. Generate a **fresh, disposable** wallet for this project only:
   ```
   python3 -c "from eth_account import Account; a=Account.create(); print(a.address, a.key.hex())"
   ``` or use metamask.
   
5. Fund that address with a small amount of Sepolia testnet ETH from a faucet (e.g. https://sepoliafaucet.com). Testnet ETH has no real value.
6. Fill in `.env` with your Gemini API key and testnet private key.

**Never put a real/mainnet private key anywhere in this project.**

## Running it

```
cd agent
python run_experiment.py
```

This runs the agent against multiple versions of the same source page: a clean control and one or more injected variants (see `malicious_sources/`): and saves a full tool-call trace for each to `findings_*.json`.

**Note:** LLM behavior isn't fully deterministic. Run it a few times and compare trace files; a single run either way isn't conclusive.

## Project structure

```
agent-security-project/
├── agent/
│   ├── agent.py            # core agent loop (undefended baseline)
│   ├── wallet_tool.py       # testnet wallet send/balance
│   ├── source_tool.py       # reads local files as stand-ins for web content
│   └── run_experiment.py    # runs control vs. injected variants side by side
├── malicious_sources/
│   ├── page1_control.txt
│   ├── page1_inject.txt
├── .env.example
└── requirements.txt
```

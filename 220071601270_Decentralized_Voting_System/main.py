"""
Decentralized Voting System - Flask Web Application
A blockchain-based voting system using Solidity smart contracts and Web3.py
"""

import json
import os
import threading
import time
from flask import Flask, flash, redirect, render_template, request, session, url_for
from eth_account import Account
from web3 import Web3
import solcx

# Flask app configuration
app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# Blockchain configuration
GANACHE_URL = 'http://127.0.0.1:8545'

# Global state
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = None
contestants = []

def ensure_blockchain_connection():
    """Ensure connection to local blockchain node."""
    if not w3.is_connected():
        raise ConnectionError("Cannot connect to local Ethereum node at " + GANACHE_URL)

def load_contract():
    """Load deployed contract from contract_address.json file."""
    global contract

    if os.path.exists('contract_address.json'):
        try:
            with open('contract_address.json', 'r') as f:
                data = json.load(f)
                contract_address = data.get('address')
                abi = data.get('abi')

                if contract_address and abi:
                    test_contract = w3.eth.contract(address=contract_address, abi=abi)
                    # Test if contract exists by calling a simple function
                    try:
                        test_contract.functions.contestantCount().call()
                        contract = test_contract
                        print(f"✅ Loaded existing contract from contract_address.json: {contract_address}")
                        return True
                    except Exception as e:
                        print(f"Contract at {contract_address} not found on current blockchain (Ganache may have restarted)")
                        print("Will deploy fresh contract to preserve voting data persistence")
        except Exception as e:
            print(f"Error loading contract from contract_address.json: {e}")

    return False

def save_contract_info(address, abi):
    """Save contract information to contract_address.json file for persistence."""
    try:
        with open('contract_address.json', 'w') as f:
            json.dump({'address': address, 'abi': abi}, f, indent=2)

        print("\n" + "="*60)
        print("✅ CONTRACT INFORMATION SAVED TO contract_address.json")
        print("="*60)
        print(f"Contract Address: {address}")
        print("\nYour votes will persist between server restarts!")
        print("="*60 + "\n")
    except Exception as e:
        print(f"Warning: Could not save contract info to contract_address.json: {e}")
        print("Contract info will be lost on server restart")

def compile_solidity_contract():
    """Compile the Solidity contract."""
    solcx.install_solc('0.8.0')
    compiled = solcx.compile_files(['contracts/Voting.sol'], output_values=['abi', 'bin'])
    contract_id, interface = compiled.popitem()
    return interface['bin'], interface['abi']

def deploy_contract():
    """Deploy the voting contract to blockchain."""
    bytecode, abi = compile_solidity_contract()
    admin_account = w3.eth.accounts[0]

    VotingContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = VotingContract.constructor().transact({'from': admin_account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress

    # Set global contract directly
    global contract
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Display contract info for secure storage
    save_contract_info(contract_address, abi)

    # Add default contestants
    default_contestants = ["Zuhair Mohammed Hussain", "Tharagaraman Balaji"]
    for name in default_contestants:
        tx = contract.functions.addContestant(name).build_transaction({
            'from': admin_account,
            'nonce': w3.eth.get_transaction_count(admin_account),
            'gas': 2000000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        send_transaction(tx, None)

    # Register default users (accounts 1-5)
    for i in range(1, 6):
        user_addr = w3.to_checksum_address(w3.eth.accounts[i])
        tx = contract.functions.registerUser(user_addr).build_transaction({
            'from': admin_account,
            'nonce': w3.eth.get_transaction_count(admin_account),
            'gas': 2000000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        send_transaction(tx, None)

    return contract_address

def refresh_contestants():
    """Update the global contestants list from blockchain."""
    global contestants
    if contract:
        count = contract.functions.contestantCount().call()
        contestants = []
        for i in range(count):
            name, votes = contract.functions.getContestant(i).call()
            contestants.append((name, votes))

def blockchain_poller():
    """Background thread to periodically update contestant data."""
    while True:
        refresh_contestants()
        time.sleep(30)

def send_transaction(tx, private_key=None):
    """Send a signed transaction and wait for confirmation."""
    if private_key:
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    else:
        # For unlocked accounts (like in Ganache)
        tx_hash = w3.eth.send_transaction(tx)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def can_user_vote(address):
    """Check if user is registered and hasn't voted yet."""
    if not contract or not address:
        return False
    try:
        checksum_addr = w3.to_checksum_address(address)
        registered, has_voted = contract.functions.users(checksum_addr).call()
        return registered and not has_voted
    except:
        return False

# Routes
@app.route('/')
def home():
    """Home page with vote tally and voting form for eligible users."""
    refresh_contestants()
    voting_allowed = can_user_vote(session.get('address')) and bool(contestants)
    return render_template('index.html', contestants=contestants, can_vote=voting_allowed)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with Ethereum address and private key."""
    if request.method == 'POST':
        address = request.form['address'].strip()
        private_key = request.form['private_key'].strip()

        try:
            account = Account.from_key(private_key)
            if account.address.lower() != address.lower():
                flash('Address does not match private key', 'error')
                return render_template('login.html')

            session['address'] = address
            session['private_key'] = private_key

            # Determine role
            if address.lower() == w3.eth.accounts[0].lower():
                session['role'] = 'admin'
                # Auto-register admin as voter
                if contract:
                    try:
                        checksum_addr = w3.to_checksum_address(address)
                        tx = contract.functions.registerUser(checksum_addr).build_transaction({
                            'from': address,
                            'nonce': w3.eth.get_transaction_count(address),
                            'gas': 2000000,
                            'gasPrice': w3.to_wei('20', 'gwei')
                        })
                        send_transaction(tx, private_key)
                    except:
                        pass  # Already registered
            else:
                session['role'] = 'user'

            flash('Login successful', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            flash('Invalid private key or address', 'error')

    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    """Admin panel for managing contestants and users."""
    if session.get('role') != 'admin':
        flash('Admin access required', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_contestant':
            name = request.form.get('name', '').strip()
            if name:
                from_addr = w3.to_checksum_address(session['address'])
                tx = contract.functions.addContestant(name).build_transaction({
                    'from': from_addr,
                    'nonce': w3.eth.get_transaction_count(from_addr),
                    'gas': 2000000,
                    'gasPrice': w3.to_wei('20', 'gwei')
                })
                send_transaction(tx, session['private_key'])
                refresh_contestants()
                flash(f'Contestant "{name}" added successfully', 'success')

        elif action == 'register_user':
            user_address = request.form.get('address', '').strip()
            if user_address:
                checksum_address = w3.to_checksum_address(user_address)
                from_addr = w3.to_checksum_address(session['address'])
                tx = contract.functions.registerUser(checksum_address).build_transaction({
                    'from': from_addr,
                    'nonce': w3.eth.get_transaction_count(from_addr),
                    'gas': 2000000,
                    'gasPrice': w3.to_wei('20', 'gwei')
                })
                send_transaction(tx, session['private_key'])
                flash(f'User {user_address} registered successfully', 'success')

    return render_template('admin.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    """Dedicated voting page (also accessible from home page form)."""
    if session.get('role') not in ['user', 'admin']:
        flash('Login required to vote', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            contestant_id = int(request.form['contestant_id'])
            from_addr = w3.to_checksum_address(session['address'])
            tx = contract.functions.vote(contestant_id).build_transaction({
                'from': from_addr,
                'nonce': w3.eth.get_transaction_count(from_addr),
                'gas': 2000000,
                'gasPrice': w3.to_wei('20', 'gwei')
            })
            send_transaction(tx, session['private_key'])
            refresh_contestants()
            flash('Vote cast successfully', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Error casting vote', 'error')

    refresh_contestants()
    return render_template('vote.html', contestants=contestants)

@app.route('/logout')
def logout():
    """Clear session and logout user."""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))

# Application startup
if __name__ == '__main__':
    ensure_blockchain_connection()

    # Try to load existing contract from contract_address.json
    if load_contract():
        print("✅ Using existing contract")
        print(f"   Contract Address: {contract.address}")
        refresh_contestants()
        print(f"   Loaded {len(contestants)} contestants")
    else:
        print("🔄 No valid contract found, deploying fresh contract...")
        deploy_contract()
        refresh_contestants()
        print("✅ Fresh contract deployed and configured")
        print("   Contract info saved to contract_address.json")

    # Start background polling
    poller = threading.Thread(target=blockchain_poller, daemon=True)
    poller.start()

    print("🚀 Starting Flask application...")
    print("   Access at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

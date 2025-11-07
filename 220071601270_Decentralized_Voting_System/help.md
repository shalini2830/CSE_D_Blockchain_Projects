# Decentralized Voting System - Codebase Documentation

## Overview

This is a blockchain-based voting system built with Python Flask, Solidity smart contracts, and Web3.py. The system allows users to vote on contestants in a decentralized manner using Ethereum blockchain technology.

## Architecture

### Core Components

1. **Flask Web Application** (`main.py`)
2. **Solidity Smart Contract** (`contracts/Voting.sol`)
3. **HTML Templates** (`templates/`)
4. **CSS Styling** (`static/main.css`)
5. **Blockchain Infrastructure** (Ganache CLI)

## Detailed Code Flow

### 1. Application Startup (`main.py`)

#### Initialization Process
```python
# 1. Load environment variables (CSS variables, config)
# 2. Initialize Flask app with configuration
app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# 3. Configure blockchain connection
GANACHE_URL = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# 4. Initialize global state
contract = None
contestants = []
```

#### Contract Loading Logic
```python
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
```

#### Contract Deployment
```python
def deploy_contract():
    """Deploy the voting contract to blockchain."""
    bytecode, abi = compile_solidity_contract()
    admin_account = w3.eth.accounts[0]

    VotingContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = VotingContract.constructor().transact({'from': admin_account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Save contract info for persistence
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
```

### 2. Smart Contract (`contracts/Voting.sol`)

#### Contract Structure
```solidity
pragma solidity ^0.8.0;

contract VotingSystem {
    address public admin;

    struct User {
        bool registered;
        bool voted;
    }

    struct Contestant {
        string name;
        uint256 voteCount;
    }

    mapping(address => User) public users;
    Contestant[] public contestants;

    event ContestantAdded(uint256 indexed id, string name);
    event UserRegistered(address indexed user);
    event VoteCast(address indexed voter, uint256 indexed contestantId);

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    modifier onlyRegistered() {
        require(users[msg.sender].registered, "User not registered");
        _;
    }

    modifier notVoted() {
        require(!users[msg.sender].voted, "User has already voted");
        _;
    }
}
```

#### Key Functions

**addContestant(string memory _name)**
- Only admin can call
- Adds new contestant to the array
- Emits ContestantAdded event

**registerUser(address _user)**
- Only admin can call
- Registers a user address for voting
- Emits UserRegistered event

**vote(uint256 _contestantId)**
- Only registered users who haven't voted
- Increments vote count for selected contestant
- Marks user as voted
- Emits VoteCast event

**getContestant(uint256 _id)**
- Returns contestant name and vote count
- View function, no gas cost

**contestantCount()**
- Returns total number of contestants
- View function

### 3. Web Routes and Logic

#### Home Route (`/`)
```python
@app.route('/')
def home():
    """Home page with vote tally and voting form for eligible users."""
    refresh_contestants()
    voting_allowed = can_user_vote(session.get('address')) and bool(contestants)
    return render_template('index.html', contestants=contestants, can_vote=voting_allowed)
```

#### Login Route (`/login`)
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
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

            # Determine role based on address
            if address.lower() == w3.eth.accounts[0].lower():
                session['role'] = 'admin'
            else:
                session['role'] = 'user'

            flash('Login successful', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            flash('Invalid private key or address', 'error')

    return render_template('login.html')
```

#### Admin Panel (`/admin`)
```python
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if session.get('role') != 'admin':
        flash('Admin access required', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_contestant':
            name = request.form.get('name', '').strip()
            if name:
                # Add contestant via smart contract
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
                # Register user via smart contract
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
```

#### Voting Route (`/vote`)
```python
@app.route('/vote', methods=['GET', 'POST'])
def vote():
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
```

### 4. Helper Functions

#### Blockchain Interaction
```python
def ensure_blockchain_connection():
    """Ensure connection to local blockchain node."""
    if not w3.is_connected():
        raise ConnectionError("Cannot connect to local Ethereum node at " + GANACHE_URL)

def send_transaction(tx, private_key=None):
    """Send a signed transaction and wait for confirmation."""
    if private_key:
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    else:
        # For unlocked accounts (like in Ganache)
        tx_hash = w3.eth.send_transaction(tx)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def refresh_contestants():
    """Update the global contestants list from blockchain."""
    global contestants
    if contract:
        count = contract.functions.contestantCount().call()
        contestants = []
        for i in range(count):
            name, votes = contract.functions.getContestant(i).call()
            contestants.append((name, votes))
```

#### User Validation
```python
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
```

### 5. Background Processes

#### Blockchain Polling
```python
def blockchain_poller():
    """Background thread to periodically update contestant data."""
    while True:
        refresh_contestants()
        time.sleep(30)  # Update every 30 seconds

# Start polling thread
poller = threading.Thread(target=blockchain_poller, daemon=True)
poller.start()
```

### 6. Data Persistence

#### Contract Information Storage
```python
def save_contract_info(address, abi):
    """Save contract information to contract_address.json file for persistence."""
    try:
        with open('contract_address.json', 'w') as f:
            json.dump({'address': address, 'abi': abi}, f, indent=2)
        print("✅ CONTRACT INFORMATION SAVED TO contract_address.json")
    except Exception as e:
        print(f"Warning: Could not save contract info to contract_address.json: {e}")
```

### 7. Frontend Templates

#### Base Template (`templates/base.html`)
- HTML5 structure with meta tags
- CSS and favicon links
- Navigation header
- Flash message display
- Content block for pages

#### Page Templates
- `index.html`: Vote tally display and voting form
- `login.html`: User authentication form
- `admin.html`: Admin controls for managing contestants and users
- `vote.html`: Dedicated voting page

### 8. CSS Styling (`static/main.css`)

#### CSS Variables
```css
:root {
    --primary: #1e40af;
    --primary-dark: #1e3a8a;
    --primary-light: #3b82f6;
    --secondary: #64748b;
    --accent: #059669;
    --success: #10b981;
    --error: #ef4444;
    --warning: #f59e0b;
    --bg-primary: #f1f5f9;
    --bg-secondary: #ffffff;
    --card-bg: #ffffff;
    --card-border: #e2e8f0;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #64748b;
    --border: #cbd5e1;
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --radius: 0.5rem;
    --radius-lg: 0.75rem;
}
```

#### Component Classes
- `.container`: Layout wrapper
- `.card`: Content containers
- `form`, `input`, `select`, `button`: Form elements
- `.table-container`, `table`, `th`, `td`: Data tables
- `.alert-success`, `.alert-error`, etc.: Flash messages

### 9. Security Features

#### Session Management
- User sessions store address, private key, and role
- Private keys are stored in session (not recommended for production)
- Role-based access control (admin vs user)

#### Input Validation
- Address checksum validation
- Private key verification
- Form input sanitization

### 10. Error Handling

#### Blockchain Connection
- Connection checks before operations
- Graceful fallback for missing contracts
- Transaction failure handling

#### User Input
- Invalid address/key combinations
- Duplicate voting prevention
- Unauthorized access attempts

## System Flow

### User Journey

1. **Start System**
   - Launch Ganache CLI with persistence
   - Run Flask application
   - Contract loads or deploys automatically

2. **Admin Setup**
   - Login with admin account (first Ganache account)
   - Add contestants via admin panel
   - Register users for voting

3. **User Voting**
   - Login with registered address and private key
   - View contestants and current vote tally
   - Cast vote (one vote per user)
   - View updated results

4. **Data Persistence**
   - Votes stored on blockchain permanently
   - Contract address saved to JSON file
   - System recovers state on restart

### Data Flow

```
User Request → Flask Route → Smart Contract Call → Blockchain Transaction → Database Update → UI Refresh
```

### Security Flow

```
User Login → Address/Key Validation → Session Creation → Role Assignment → Access Control → Contract Interaction
```

## Dependencies

### Python Packages (`requirements.txt`)
- Flask==2.3.3: Web framework
- web3==6.0.0: Blockchain interaction
- py-solc-x==1.1.1: Solidity compilation
- eth-account==0.8.0: Ethereum account management

### External Dependencies
- Ganache CLI: Local Ethereum testnet
- Node.js: For running Ganache
- Solidity Compiler: For contract compilation

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask session secret (currently hardcoded)
- `GANACHE_URL`: Blockchain node URL (default: http://127.0.0.1:8545)

### File Structure
```
project_root/
├── main.py                 # Main Flask application
├── contract_address.json   # Contract persistence
├── start-ganache.sh        # Ganache startup script
├── ganache-db/             # Blockchain database
├── contracts/
│   └── Voting.sol          # Smart contract
├── static/
│   └── main.css            # Stylesheet
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── login.html          # Login page
│   ├── admin.html          # Admin panel
│   └── vote.html           # Voting page
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md               # Documentation
```

## Deployment Considerations

### Development
- Use `start-ganache.sh` for persistent blockchain
- Run with `python main.py`
- Access at `http://127.0.0.1:5000`

### Production
- Use production blockchain (not Ganache)
- Implement secure key management
- Add HTTPS and proper authentication
- Use production WSGI server (Gunicorn, uWSGI)

### Security Improvements Needed
- Remove private key storage from sessions
- Implement proper user authentication
- Add rate limiting and DDoS protection
- Use environment variables for secrets
- Implement input sanitization and validation
- Add logging and monitoring

This documentation provides a comprehensive overview of how the Decentralized Voting System works, from the initial setup to the voting process and data persistence.

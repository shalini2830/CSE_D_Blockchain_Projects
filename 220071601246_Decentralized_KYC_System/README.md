# Decentralized KYC Portal  
### A Blockchain-Based System for Secure Identity Verification  

## TEAM MEMBERS
- **Salman** – RRN: 220071601216  
- **Sidharth H** – RRN: 220071601246  
- **Syed Ibrahim B** – RRN: 220071601259  
- **Syed Roshan** – RRN: 220071601261  
- **Syed Galib** – RRN: 220071601257  

**B.Tech – CSE D**  
**November 2025**

---

# Project Overview

The **Decentralized KYC Portal** is a blockchain-powered identity verification system built to simplify and secure the KYC process for banks and financial institutions.

Traditional KYC is slow, repetitive, and requires customers to submit documents to every institution separately. Our system allows users to complete KYC once and securely share verification with any bank using blockchain technology.

## Key Highlights

- **Tamper-Proof Data:** KYC details stored on the blockchain cannot be modified or forged.  
- **One-Time KYC:** Customers register once; multiple banks can verify it.  
- **Permission-Based Access:** Only the customer approves who can view their KYC data.  
- **Smart Contract Automation:** Handles KYC registration, verification, and status updates.  
- **Transparent & Secure:** Blockchain ensures trust without intermediaries.

## Real-World Use Cases
- Banking customer onboarding  
- Loan verification  
- Telecom SIM registration  
- Fintech app verification  
- Insurance onboarding  
- Government ID verification  

---

# Workflow

### **1. Register Customer**
User enters name, age, email, Aadhar, and submits KYC details.

### **2. Bank Requests Verification**
A financial institution submits a request to view user KYC.

### **3. Customer Approves/Rejects**
User controls access and grants the bank permission.

### **4. Bank Verifies KYC**
Once approved, the bank can mark the KYC as **Verified** or **Rejected**.

### **5. Update/Re-Verify**
Users can update details; banks may request re-verification.

---

# Output Format

Smart contract returns the KYC record in structured form:

```json
{
  "name": "John Doe",
  "age": 27,
  "email": "john@example.com",
  "aadhar": "xxxx-xxxx-xxxx",
  "kycStatus": "verified",
  "verifiedBy": "0x1234abcd...ef90",
  "dataHash": "Qmxxxxxxxxxxxxxxxxxxxx",
  "lastUpdated": 1732652815
}
```

---

# Technology Stack

### Blockchain
- Solidity  
- Ethereum / Ganache  
- Truffle Framework  

### Frontend
- React.js  
- Web3.js  
- MetaMask  

### Tools
- Node.js  
- NPM  
- VS Code  
- Git / GitHub  

---

# Smart Contract Features

- Customer registration  
- Bank verification workflow  
- Document hash storage (off-chain)  
- Immutable KYC records  
- Permissioned access control  
- Event logging for transparency  

---

# How to Run the Project

### 1. Clone Repository
```bash
git clone <repository-url>
cd Decentralized-KYC-Portal
```

### 2. Start Local Blockchain
Open **Ganache** and start a workspace.

### 3. Compile & Deploy Contracts
```bash
cd blockchain
truffle compile
truffle migrate --reset
```

### 4. Start Frontend
```bash
cd ../frontend
npm install
npm start
```

Connect MetaMask to:
```
Network: Ganache Local
RPC: http://127.0.0.1:7545
Chain ID: 5777 or 1337
```

---

# Screenshots Included
The repository includes screenshots showing:
- Smart contract deployment  
- MetaMask connection  
- KYC registration  
- KYC status verification  
- Ganache transaction logs  

---

# Conclusion

The **Decentralized KYC Portal** showcases how blockchain can revolutionize identity verification by ensuring security, transparency, and user control. The project provides a future-ready solution for the banking sector and other industries where reliable identity verification is essential.

---


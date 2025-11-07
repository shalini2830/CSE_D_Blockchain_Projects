FraudBlock: Blockchain-Based Fake Product Identification Using QR Code

TEAM MEMBERS

Salha Afreen Sahani - 220071601215

Sana Taquim - 220071601220

Shree Shivani M - 220071601241

Usashi Amant  - 220071601268

Yeshikasri K - 220071601272



Project Overview



This project is a blockchain-based product authentication system that prevents the circulation of counterfeit goods. FraudBlock enables manufacturers to generate unique QR codes for each product and records their authenticity on a blockchain. Consumers can then scan these QR codes to verify whether the product is genuine or fake, ensuring transparency, traceability, and trust across the supply chain.



Key highlights of the project:



Tamper-Proof Product Records: Each product’s information is stored on the blockchain, making it immutable and secure.



QR Code Verification: Every product has a unique QR code linked to its blockchain record, allowing easy authenticity checks.



Decentralized Validation: Product verification does not depend on a centralized server — authenticity is checked directly from the blockchain.



Consumer Transparency: Buyers can instantly verify product legitimacy before purchase using any blockchain-enabled web interface.



Manufacturer Dashboard: Provides manufacturers the ability to register new products, generate QR codes, and track authenticity.



Smart Contract Integration: Uses Ethereum-based smart contracts to ensure permanent and verifiable product registration.



Blockchain Security: Ensures trust, transparency, and resistance to forgery through distributed ledger technology.



This system models a real-world blockchain-based anti-counterfeit solution, making product verification simple, secure, and efficient.



Workflow

1\. Register Manufacturer



Manufacturers are registered with unique blockchain wallet addresses and are authorized to add genuine product entries into the system.



2\. Add Product and Generate QR Code



Each product is added with a unique product ID and essential details.

Upon registration, a QR code is generated and linked to the blockchain transaction that stores the product’s authenticity record.



3\. Verify Product Authenticity



Consumers scan the product’s QR code using the web interface.

The system queries the blockchain through Web3.js and verifies the product’s authenticity directly from the smart contract.



4\. Detect Counterfeit Products



If a scanned product ID does not exist on the blockchain or has mismatched details, it is flagged as fake or unauthorized.



5\. Transparency for All



Both manufacturers and consumers can track the product’s lifecycle and authenticity without depending on third-party authorities.



Output Format



When a product QR code is scanned and verified, the system provides structured output in JSON format:



{

&nbsp; "productId": "prod-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",

&nbsp; "productName": "ABC Luxury Watch",

&nbsp; "manufacturer": "XYZ Corporation",

&nbsp; "authenticity": "genuine",

&nbsp; "blockchainTransaction": "0xabcdef1234567890abcdef1234567890abcdef12"

}





If a product is fake or not found, the output will be:



{

&nbsp; "productId": "prod-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",

&nbsp; "status": "fake or unregistered"

}



Technologies Used



Blockchain Platform: Ethereum (Local Network via Ganache)



Smart Contract Language: Solidity



Smart Contract Framework: Truffle



Frontend: HTML, CSS, JavaScript



Blockchain Interaction: Web3.js



Local Blockchain Simulator: Ganache



Wallet Integration: MetaMask



Runtime Environment: Node.js



System Requirements



Node.js (v16 or above)



Truffle (v5 or above)



Ganache (v7 or above)



MetaMask Extension on Chrome/Brave/Edge



Steps to Run



Clone the repository:



git clone https://github.com/yogeshxd/FraudBlock

cd FraudBlock





Install dependencies:



npm install





Start Ganache:



Create a new workspace.



Import project configuration.



Check that the port (default 7545) matches the one in truffle-config.js.



Connect MetaMask:



Add a new network with RPC URL http://127.0.0.1:7545.



Network ID: 5777



Import one of the Ganache accounts using its private key.



Compile and migrate smart contracts:



truffle compile

truffle migrate





Run the web app:



npm run dev





Then open http://localhost:3000 (or whichever port is shown).



Sample Use Case



Scenario:

A luxury brand registers its watches on the blockchain. Each watch has a QR code linked to a blockchain transaction.

When a customer scans the QR code:



If the product is legitimate → “Product Verified: Genuine.”



If the product is missing or tampered → “Product Verification Failed: Fake Product Detected.”


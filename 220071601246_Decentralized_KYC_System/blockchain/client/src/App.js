import React, { useEffect, useState } from "react";
import Web3 from "web3";
import KYC from  "./build/contracts/KYC.json"; // Adjust path if needed

function App() {
  const [account, setAccount] = useState("");
  const [contract, setContract] = useState(null);
  const [message, setMessage] = useState("");

  // Load Web3 + Contract
  useEffect(() => {
    loadBlockchainData();
  }, []);

  const loadBlockchainData = async () => {
    if (window.ethereum) {
      const web3 = new Web3(window.ethereum);
      await window.ethereum.request({ method: "eth_requestAccounts" });

      const accounts = await web3.eth.getAccounts();
      setAccount(accounts[0]);

      const networkId = await web3.eth.net.getId();
      const networkData = KYC.networks[networkId];

      if (networkData) {
        const contractInstance = new web3.eth.Contract(
          KYC.abi,
          networkData.address
        );
        setContract(contractInstance);
        setMessage("Contract loaded successfully!");
      } else {
        setMessage("Smart contract not deployed to detected network.");
      }
    } else {
      setMessage("Please install MetaMask!");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Decentralized KYC System</h2>
      <p><strong>Account:</strong> {account}</p>
      <p>{message}</p>
    </div>
  );
}

export default App;

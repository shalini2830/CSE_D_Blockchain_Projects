import React, { useEffect, useState } from "react";
import web3 from "./ethereum";
import loadContract from "./contract";
import "./index.css";

function App() {
  const [account, setAccount] = useState("");
  const [contract, setContract] = useState(null);
  const [input, setInput] = useState({
    name: "",
    age: "",
    email: "",
    aadhar: ""
  });
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  // ✅ Initialize Wallet + Contract
  useEffect(() => {
    async function init() {
      const accounts = await web3.eth.getAccounts();
      setAccount(accounts[0]);

      const instance = await loadContract();
      if (!instance) {
        alert("Contract not deployed on this network!");
        return;
      }
      setContract(instance);
    }

    init();
  }, []);

  // ✅ Register KYC
  const register = async () => {
    if (!contract) return alert("Contract not loaded");

    if (!input.name || !input.age || !input.email || !input.aadhar) {
      alert("All fields are required!");
      return;
    }

    setLoading(true);
    try {
      await contract.methods
        .registerUser(input.name, Number(input.age), input.email, input.aadhar)
        .send({ from: account });

      alert("KYC Registered Successfully ✅");
      setStatus("Registered ✅");
    } catch (err) {
      alert("Transaction Failed: " + err.message);
    }
    setLoading(false);
  };

  // ✅ Check KYC Status
  const check = async () => {
    if (!contract) return alert("Contract not loaded");

    const user = await contract.methods.getUser(account).call();

    setStatus(user[4] ? "Registered ✅" : "Not Registered ❌");
  };

  return (
    <div className="app-container">
      
      {/* ✅ LEFT PANEL */}
      <div className="side-panel left-panel">
        <h2>Project Info</h2>
        <ul>
          <li>Decentralized KYC</li>
          <li>Blockchain Verified</li>
          <li>Secure Identity Storage</li>
          <li>Real-time Status Check</li>
        </ul>
      </div>

      {/* ✅ MAIN CARD */}
      <div className="kyc-card">
        <h1 className="title">🛸 Simple KYC Portal</h1>

        <p className="wallet">
          Connected Wallet: <span>{account || "Not Connected"}</span>
        </p>

        {/* ✅ Registration Form */}
        <div className="form-section">
          <h2>Register for KYC</h2>

          <div className="input-group">
            <input
              type="text"
              value={input.name}
              onChange={(e) => setInput({ ...input, name: e.target.value })}
            />
            <label>Full Name</label>
          </div>

          <div className="input-group">
            <input
              type="number"
              value={input.age}
              onChange={(e) => setInput({ ...input, age: e.target.value })}
            />
            <label>Age</label>
          </div>

          <div className="input-group">
            <input
              type="email"
              value={input.email}
              onChange={(e) => setInput({ ...input, email: e.target.value })}
            />
            <label>Email</label>
          </div>

          <div className="input-group">
            <input
              type="text"
              value={input.aadhar}
              onChange={(e) => setInput({ ...input, aadhar: e.target.value })}
            />
            <label>Aadhar</label>
          </div>

          <button onClick={register} disabled={loading} className="glow-btn">
            {loading ? "Processing..." : "Submit KYC"}
          </button>
        </div>

        <hr />

        {/* ✅ Check Status */}
        <div className="form-section">
          <h2>Check KYC Status</h2>
          <button onClick={check} className="glow-btn neon-purple">
            Check My Status
          </button>

          {status && (
            <div className={`status-badge`}>
              Status: {status}
            </div>
          )}
        </div>
      </div>

      {/* ✅ RIGHT PANEL */}
      <div className="side-panel right-panel">
        <h2>Recent Activity</h2>
        <p>✅ User registration logs</p>
        <p>✅ Status updates</p>
        <p>✅ Blockchain events</p>
      </div>

    </div>
  );
}

export default App;

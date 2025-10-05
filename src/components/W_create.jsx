// src/App.jsx
import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:4000"; // Change if deployed

function App() {
  const [wallet, setWallet] = useState(""); // user's wallet address
  const [balance, setBalance] = useState(null);
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState("");
  const [transactions, setTransactions] = useState([]);
  const [mnemonic, setMnemonic] = useState("");

  // Generate 12-word mnemonic (mock)
  const generateMnemonic = () => {
    const words = "apple banana cat dog egg fish grape hat ice jam kite lime".split(" ");
    setMnemonic(words.sort(() => 0.5 - Math.random()).join(" "));
  };

  // Create wallet on backend
  const createWallet = async () => {
    if (!wallet) {
      alert("Please enter your wallet address");
      return;
    }
    try {
      const res = await axios.post(`${API_BASE}/create_wallet`, { address: wallet });
      setBalance(res.data.balance_eth);
      alert("Wallet created successfully!");
    } catch (err) {
      console.error(err);
      alert("Error creating wallet: " + err.response?.data?.error || err.message);
    }
  };

  // Fetch balance
  const fetchBalance = async () => {
    if (!wallet) {
      alert("Enter wallet address");
      return;
    }
    try {
      const res = await axios.get(`${API_BASE}/balance/${wallet}`);
      setBalance(res.data.balance_eth);
    } catch (err) {
      console.error(err);
      alert("Error fetching balance: " + err.response?.data?.error || err.message);
    }
  };

  // Send ETH
  const sendEth = async () => {
    if (!wallet || !recipient || !amount) {
      alert("Fill in all fields");
      return;
    }
    try {
      await axios.post(`${API_BASE}/send_eth`, {
        sender: wallet,
        recipient,
        amount,
      });
      alert("Transfer successful!");
      fetchBalance(); // update balance
      fetchTransactions(); // update history
    } catch (err) {
      console.error(err);
      alert("Error sending ETH: " + err.response?.data?.error || err.message);
    }
  };

  // Fetch transaction history
  const fetchTransactions = async () => {
    if (!wallet) return;
    try {
      const res = await axios.get(`${API_BASE}/transactions/${wallet}`);
      setTransactions(res.data.transactions);
    } catch (err) {
      console.error(err);
      alert("Error fetching transactions: " + err.response?.data?.error || err.message);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h1>Mock Web3 Wallet</h1>

      {/* Create Wallet */}
      <div style={{ marginBottom: 20 }}>
        <h3>Create Wallet</h3>
        <button onClick={generateMnemonic}>Generate 12-word mnemonic</button>
        {mnemonic && <p><strong>Mnemonic:</strong> {mnemonic}</p>}
        <input
          type="text"
          placeholder="Enter wallet address"
          value={wallet}
          onChange={(e) => setWallet(e.target.value)}
          style={{ width: "100%", marginBottom: 10 }}
        />
        <button onClick={createWallet}>Create Wallet on Server</button>
      </div>

      {/* Fetch Balance */}
      <div style={{ marginBottom: 20 }}>
        <h3>Retrieve Wallet Balance</h3>
        <button onClick={fetchBalance}>Fetch Balance</button>
        {balance !== null && <p><strong>Balance:</strong> {balance} ETH</p>}
      </div>

      {/* Send ETH */}
      <div style={{ marginBottom: 20 }}>
        <h3>Send Mock ETH</h3>
        <input
          type="text"
          placeholder="Recipient address"
          value={recipient}
          onChange={(e) => setRecipient(e.target.value)}
          style={{ width: "100%", marginBottom: 10 }}
        />
        <input
          type="number"
          placeholder="Amount in ETH"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          style={{ width: "100%", marginBottom: 10 }}
        />
        <button onClick={sendEth}>Send ETH</button>
      </div>

      {/* Transaction History */}
      <div style={{ marginBottom: 20 }}>
        <h3>Transaction History</h3>
        <button onClick={fetchTransactions}>Fetch History</button>
        {transactions.length > 0 ? (
          <ul>
            {transactions.map((tx) => (
              <li key={tx.id}>
                {tx.timestamp}: {tx.sender} → {tx.recipient} : {tx.amount} ETH
              </li>
            ))}
          </ul>
        ) : (
          <p>No transactions yet.</p>
        )}
      </div>
    </div>
  );
}

export default App;

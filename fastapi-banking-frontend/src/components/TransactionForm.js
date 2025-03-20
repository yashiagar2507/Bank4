import React, { useState } from "react";
import axios from "axios";

const TransactionForm = () => {
  const [accountId, setAccountId] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleTransaction = async (type) => {
    try {
      const response = await axios.post(`http://localhost:8000/transactions/${type}`, {
        account_id: accountId,
        amount: parseFloat(amount),
      });

      setMessage(response.data.message);
      setError(""); // Clear error if successful
    } catch (err) {
      setError(err.response?.data?.detail || "Transaction failed");
      setMessage(""); // Clear message if error occurs
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h2 className="text-lg font-semibold">Make a Transaction</h2>

      <input
        type="text"
        placeholder="Enter Account ID"
        value={accountId}
        onChange={(e) => setAccountId(e.target.value)}
        className="border p-2 w-full rounded"
      />

      <input
        type="number"
        placeholder="Enter Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        className="border p-2 w-full rounded"
      />

      <button onClick={() => handleTransaction("credit")} className="bg-green-500 text-white px-4 py-2 rounded mr-2">
        Credit
      </button>
      <button onClick={() => handleTransaction("debit")} className="bg-red-500 text-white px-4 py-2 rounded">
        Debit
      </button>

      {message && <p className="text-green-500 mt-2">{message}</p>}
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
};

export default TransactionForm;

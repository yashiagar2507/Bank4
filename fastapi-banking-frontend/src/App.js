import React from "react";
import TransactionForm from "./components/TransactionForm";

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-6">FastAPI AI-Rate Limited Banking System</h1>
      <TransactionForm />
    </div>
  );
}

export default App;

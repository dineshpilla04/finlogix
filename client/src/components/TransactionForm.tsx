import { useState } from "react";
import api from "../services/api";

export default function TransactionForm({ onSuccess }: { onSuccess: () => void }) {
  const [type, setType] = useState("income");
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [note, setNote] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/transactions", {
        type,
        amount: parseFloat(amount),
        category,
        note,
      });
      onSuccess();
      setAmount(""); setCategory(""); setNote("");
    } catch {
      alert("Failed to add transaction");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Add Transaction</h3>
      <select value={type} onChange={(e) => setType(e.target.value)}>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Note"
        value={note}
        onChange={(e) => setNote(e.target.value)}
      />
      <button type="submit">Add</button>
    </form>
  );
}

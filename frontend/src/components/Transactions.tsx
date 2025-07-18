import * as React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';

interface Transaction {
  id: number;
  amount: number;
  category: string;
  note: string;
  type: 'income' | 'expense';
  timestamp: string;
}

const Transactions: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('');
  const [note, setNote] = useState('');
  const [type, setType] = useState<'income' | 'expense'>('expense');
  const [error, setError] = useState('');
  const { token } = useAuth();

  const fetchTransactions = async () => {
    try {
      const response = await axios.get('/transactions', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [token]);

  const handleAddTransaction = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!amount || !category) {
      setError('Amount and category are required');
      return;
    }
    try {
      await axios.post(
        '/transactions',
        {
          amount: parseFloat(amount),
          category,
          note,
          type,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setAmount('');
      setCategory('');
      setNote('');
      setType('expense');
      fetchTransactions();
    } catch (error) {
      setError('Failed to add transaction');
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4">Transactions</h2>
      <form onSubmit={handleAddTransaction} className="mb-6">
        {error && <p className="text-red-600 mb-2">{error}</p>}
        <div className="mb-2">
          <label className="block mb-1">Amount</label>
          <input
            type="number"
            step="0.01"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="border p-2 w-full"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Category</label>
          <input
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="border p-2 w-full"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block mb-1">Note</label>
          <input
            type="text"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            className="border p-2 w-full"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Type</label>
          <select
            value={type}
            onChange={(e) => setType(e.target.value as 'income' | 'expense')}
            className="border p-2 w-full"
          >
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
        </div>
        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Add Transaction
        </button>
      </form>
      {transactions.length === 0 ? (
        <p>No transactions found.</p>
      ) : (
        <ul>
          {transactions.map((t) => (
            <li key={t.id} className="mb-2 border-b pb-2">
              <p>
                <strong>{t.type.toUpperCase()}</strong> - ${t.amount.toFixed(2)} - {t.category}
              </p>
              {t.note && <p>Note: {t.note}</p>}
              <p className="text-sm text-gray-500">{new Date(t.timestamp).toLocaleString()}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Transactions;

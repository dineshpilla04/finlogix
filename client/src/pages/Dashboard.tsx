import { useEffect, useState } from "react";
import api from "../services/api";
import TransactionForm from "../components/TransactionForm";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import socket from "../services/socket";
ChartJS.register(ArcElement, Tooltip, Legend);

interface Transaction {
  id: number;
  type: "income" | "expense";
  amount: number;
  category: string;
  note: string;
  timestamp: string;
}

export default function Dashboard() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  const fetchTransactions = async () => {
    try {
      const res = await api.get("/transactions");
      setTransactions(res.data);
    } catch {
      alert("Could not fetch transactions");
    }
  };

  useEffect(() => {
    fetchTransactions();

    socket.connect();
    socket.on("new_transaction", () => {
      fetchTransactions();
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const totals: { [key: string]: number } = {};
  transactions.forEach(t => {
    totals[t.category] = (totals[t.category] || 0) + t.amount;
  });

  const chartData = {
    labels: Object.keys(totals),
    datasets: [{
      data: Object.values(totals),
      backgroundColor: ["#4caf50", "#f44336", "#2196f3", "#ff9800"],
    }]
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Dashboard</h1>
      <TransactionForm onSuccess={() => {}} />
      <h3>Recent Transactions</h3>
      <ul>
        {transactions.map(t => (
          <li key={t.id}>
            ₹{t.amount} ({t.type}) - {t.category} - {t.note}
          </li>
        ))}
      </ul>
      <h3>Spending Breakdown</h3>
      <Pie data={chartData} />
    </div>
  );
}

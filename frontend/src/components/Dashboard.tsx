import * as React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.tsx';
import { Pie, Bar } from 'react-chartjs-2';
import { Chart, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';

Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

interface Summary {
  total_income: number;
  total_expense: number;
  balance: number;
  category_breakdown: { [key: string]: number };
}

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<Summary | null>(null);

  const { token } = useAuth();

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await axios.get('/dashboard/summary', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching dashboard summary:', error);
      }
    };
    fetchSummary();
  }, [token]);

  if (!summary) {
    return <div>Loading...</div>;
  }

  const pieData = {
    labels: Object.keys(summary.category_breakdown),
    datasets: [
      {
        data: Object.values(summary.category_breakdown),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#C9CBCF',
        ],
      },
    ],
  };

  const barData = {
    labels: ['Income', 'Expense'],
    datasets: [
      {
        label: 'Amount',
        data: [summary.total_income, summary.total_expense],
        backgroundColor: ['#36A2EB', '#FF6384'],
      },
    ],
  };

  return (
    <div className="p-4">
      <nav className="mb-4 flex justify-between items-center">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <div className="flex gap-4">
          <a
            href="/transactions"
            className="text-blue-600 hover:underline"
          >
            Transactions
          </a>
          <a
            href="/chat"
            className="text-blue-600 hover:underline"
          >
            AI Budget Chat
          </a>
        </div>
      </nav>
      <div className="mb-4">
        <p><strong>Balance:</strong> ₹{summary.balance.toFixed(2)}</p>
        <p><strong>Total Income:</strong> ₹{summary.total_income.toFixed(2)}</p>
        <p><strong>Total Expense:</strong> ₹{summary.total_expense.toFixed(2)}</p>
      </div>
      <div className="flex flex-wrap gap-8">
        <div className="w-full md:w-1/2">
          <h3 className="text-xl font-semibold mb-2">Spending by Category</h3>
          <Pie data={pieData} />
        </div>
        <div className="w-full md:w-1/2">
          <h3 className="text-xl font-semibold mb-2">Income vs Expense</h3>
          <Bar data={barData} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

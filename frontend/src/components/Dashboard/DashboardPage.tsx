import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../Common/Layout';
import { useAuth } from '../../hooks/useAuth';
import { useExperiments } from '../../hooks/useExperiments';

interface QuickActionCard {
  title: string;
  description: string;
  to: string;
  icon: string;
  color: string;
}

const QUICK_ACTIONS: QuickActionCard[] = [
  {
    title: 'New Experiment',
    description: 'Create and configure a new experiment',
    to: '/experiments',
    icon: '🧪',
    color: 'bg-blue-50 border-blue-200 hover:bg-blue-100',
  },
  {
    title: 'Upload Data',
    description: 'Upload imaging, CRISPR, Tn-seq or metadata files',
    to: '/upload',
    icon: '📂',
    color: 'bg-green-50 border-green-200 hover:bg-green-100',
  },
  {
    title: 'View Analysis',
    description: 'Explore analysis results and statistics',
    to: '/analysis',
    icon: '📊',
    color: 'bg-purple-50 border-purple-200 hover:bg-purple-100',
  },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const { total, loading } = useExperiments();

  return (
    <Layout>
      {/* Welcome banner */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.full_name || user?.username}!
        </h1>
        <p className="mt-1 text-gray-500">
          M. abscessus Antibiotic Tolerance Research Platform
        </p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <StatCard
          label="Experiments"
          value={loading ? '…' : String(total)}
          icon="🧫"
          color="text-blue-700"
        />
        <StatCard label="Your Role" value={user?.role ?? '—'} icon="👤" color="text-purple-700" />
        <StatCard
          label="Account Status"
          value={user?.is_active ? 'Active' : 'Inactive'}
          icon="✅"
          color="text-green-700"
        />
      </div>

      {/* Quick actions */}
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h2>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {QUICK_ACTIONS.map(({ title, description, to, icon, color }) => (
          <Link
            key={to}
            to={to}
            className={`card border transition-colors ${color} flex flex-col gap-2`}
          >
            <span className="text-3xl">{icon}</span>
            <h3 className="text-base font-semibold text-gray-800">{title}</h3>
            <p className="text-sm text-gray-600">{description}</p>
          </Link>
        ))}
      </div>
    </Layout>
  );
}

function StatCard({
  label,
  value,
  icon,
  color,
}: {
  label: string;
  value: string;
  icon: string;
  color: string;
}) {
  return (
    <div className="card flex items-center gap-4">
      <span className="text-3xl">{icon}</span>
      <div>
        <p className="text-xs text-gray-500 uppercase tracking-wide">{label}</p>
        <p className={`text-2xl font-bold capitalize ${color}`}>{value}</p>
      </div>
    </div>
  );
}

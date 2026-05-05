import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ScatterChart,
  Scatter,
  ResponsiveContainer,
} from 'recharts';
import Layout from '../Common/Layout';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';
import { useVisualization } from '../../hooks/useVisualization';

const TABS = ['Survival Curve', 'Heatmap', 'Time-Kill', 'Scatter', 'Images', 'Network'] as const;
type Tab = typeof TABS[number];

const COLORS = ['#2563eb', '#16a34a', '#dc2626', '#9333ea', '#ea580c', '#0891b2'];

export default function VisualizationPage() {
  const { id } = useParams<{ id: string }>();
  const experimentId = Number(id);
  const [activeTab, setActiveTab] = useState<Tab>('Survival Curve');

  const { survivalCurve, heatmap, timeKill, scatter, images, network, loading, error } =
    useVisualization(experimentId);

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">
        Visualizations — Experiment #{id}
      </h1>

      {/* Tab bar */}
      <div className="flex gap-1 border-b border-gray-200 mb-6 overflow-x-auto">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 text-sm font-medium whitespace-nowrap transition-colors ${
              activeTab === tab
                ? 'border-b-2 border-blue-600 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {loading && <LoadingSpinner />}
      {error && !loading && <ErrorMessage message={error} />}

      {!loading && (
        <div className="card min-h-[400px]">
          {activeTab === 'Survival Curve' && (
            <ChartPanel title="Survival Curve" hasData={!!survivalCurve?.length}>
              <ResponsiveContainer width="100%" height={360}>
                <LineChart data={survivalCurve ?? []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" label={{ value: 'Time', position: 'insideBottom', offset: -4 }} />
                  <YAxis label={{ value: 'Survival (%)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="survival" stroke={COLORS[0]} strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </ChartPanel>
          )}

          {activeTab === 'Heatmap' && (
            <ChartPanel title="Heatmap" hasData={!!heatmap}>
              {heatmap ? (
                <HeatmapGrid data={heatmap} />
              ) : (
                <Placeholder />
              )}
            </ChartPanel>
          )}

          {activeTab === 'Time-Kill' && (
            <ChartPanel title="Time-Kill Curve" hasData={!!timeKill?.length}>
              <ResponsiveContainer width="100%" height={360}>
                <LineChart data={timeKill ?? []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" label={{ value: 'Time (h)', position: 'insideBottom', offset: -4 }} />
                  <YAxis label={{ value: 'CFU/mL', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="cfu" stroke={COLORS[1]} strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </ChartPanel>
          )}

          {activeTab === 'Scatter' && (
            <ChartPanel title="Scatter Plot" hasData={!!scatter?.length}>
              <ResponsiveContainer width="100%" height={360}>
                <ScatterChart>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="x" name="X" />
                  <YAxis dataKey="y" name="Y" />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                  <Scatter data={scatter ?? []} fill={COLORS[2]} />
                </ScatterChart>
              </ResponsiveContainer>
            </ChartPanel>
          )}

          {activeTab === 'Images' && (
            <ChartPanel title="Microscopy Images" hasData={!!images?.length}>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                {(images ?? []).map((img) => (
                  <div key={img.id} className="rounded-lg overflow-hidden border border-gray-200">
                    <img
                      src={img.url}
                      alt={img.description ?? img.filename}
                      className="w-full h-40 object-cover bg-gray-100"
                    />
                    <p className="text-xs text-gray-600 p-2 truncate">{img.filename}</p>
                  </div>
                ))}
              </div>
            </ChartPanel>
          )}

          {activeTab === 'Network' && (
            <ChartPanel title="Gene Interaction Network" hasData={!!network}>
              {network ? (
                <NetworkInfo data={network} />
              ) : (
                <Placeholder />
              )}
            </ChartPanel>
          )}
        </div>
      )}
    </Layout>
  );
}

function ChartPanel({
  title,
  hasData,
  children,
}: {
  title: string;
  hasData: boolean;
  children: React.ReactNode;
}) {
  return (
    <div>
      <h2 className="text-base font-semibold text-gray-800 mb-4">{title}</h2>
      {hasData ? children : <Placeholder />}
    </div>
  );
}

function Placeholder() {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-gray-400">
      <span className="text-4xl mb-3">📉</span>
      <p className="text-sm">No data available for this experiment yet.</p>
    </div>
  );
}

function HeatmapGrid({ data }: { data: { rows: string[]; columns: string[]; values: number[][] } }) {
  const max = Math.max(...data.values.flat());
  const min = Math.min(...data.values.flat());

  function cellColor(val: number): string {
    const norm = max === min ? 0.5 : (val - min) / (max - min);
    const r = Math.round(255 * norm);
    const b = Math.round(255 * (1 - norm));
    return `rgb(${r}, 50, ${b})`;
  }

  return (
    <div className="overflow-auto">
      <table className="text-xs border-collapse">
        <thead>
          <tr>
            <th className="p-1" />
            {data.columns.map((col) => (
              <th key={col} className="p-1 text-gray-600 font-medium whitespace-nowrap">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.rows.map((row, ri) => (
            <tr key={row}>
              <td className="p-1 pr-3 text-gray-600 font-medium whitespace-nowrap">{row}</td>
              {data.values[ri].map((val, ci) => (
                <td
                  key={ci}
                  title={String(val)}
                  className="w-8 h-8"
                  style={{ backgroundColor: cellColor(val) }}
                />
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function NetworkInfo({ data }: { data: { nodes: unknown[]; edges: unknown[] } }) {
  return (
    <div className="text-sm text-gray-700 space-y-2">
      <p>
        <strong>Nodes:</strong> {data.nodes.length}
      </p>
      <p>
        <strong>Edges:</strong> {data.edges.length}
      </p>
      <p className="text-gray-400 mt-4">
        Interactive network graph rendering is available in the full analysis module.
      </p>
    </div>
  );
}

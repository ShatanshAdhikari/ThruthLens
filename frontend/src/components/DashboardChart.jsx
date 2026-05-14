import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const DashboardChart = ({ claims }) => {
  if (!claims || claims.length === 0) return null;

  const data = claims.map((c, i) => ({
    name: `Claim ${i + 1}`,
    risk: c.risk_score * 100,
  }));

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" />
          <YAxis unit="%" />
          <Tooltip 
            formatter={(value) => [`${value.toFixed(1)}%`, 'Risk Score']}
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
          />
          <Bar dataKey="risk">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.risk > 70 ? '#ef4444' : entry.risk > 30 ? '#f59e0b' : '#10b981'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DashboardChart;

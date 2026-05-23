import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const DashboardChart = ({ claims }) => {
  if (!claims || claims.length === 0) {
    return (
      <div className="h-64 w-full flex items-center justify-center bg-slate-50 rounded-lg border border-dashed border-slate-300 text-slate-400">
        No claims to visualize
      </div>
    );
  }

  const data = claims.map((c, i) => ({
    name: c.claim.length > 20 ? `${c.claim.substring(0, 17)}...` : c.claim,
    fullClaim: c.claim,
    risk: Math.round(c.risk_score * 100),
  }));

  return (
    <div className="h-72 w-full mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
          <XAxis 
            dataKey="name" 
            angle={-45} 
            textAnchor="end" 
            interval={0} 
            height={80}
            tick={{ fontSize: 10, fontWeight: 600, fill: '#64748b' }}
          />
          <YAxis 
            unit="%" 
            domain={[0, 100]}
            tick={{ fontSize: 11, fontWeight: 600, fill: '#64748b' }}
          />
          <Tooltip 
            cursor={{ fill: '#f8fafc' }}
            formatter={(value) => [`${value}%`, 'Hallucination Risk']}
            contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)', padding: '12px' }}
            labelStyle={{ fontWeight: 'bold', marginBottom: '4px', color: '#1e293b' }}
          />
          <Bar dataKey="risk" radius={[6, 6, 0, 0]} barSize={40}>
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={entry.risk > 70 ? '#ef4444' : entry.risk > 30 ? '#f59e0b' : '#10b981'} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DashboardChart;

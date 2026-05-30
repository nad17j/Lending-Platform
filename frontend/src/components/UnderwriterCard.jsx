// src/components/UnderwriterCard.jsx
import React from 'react';

export default function UnderwriterCard({ metrics, status = 'PENDING' }) {
  // Matches exact backend multi-agent orchestrator output state
  const isEscalated = status === 'ESCALATED TO HUMAN REVIEW';

  // Safely format currencies into standard local presentation layouts
  const formatCurrency = (value) => {
    if (value === undefined || value === null) return '0.00';
    return new Intl.NumberFormat('en-LK', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value);
  };

  // Convert fractional backend DTI decimals (e.g., 0.40) to standard percentage integers (40%)
  const displayDti = metrics?.dti_ratio !== undefined ? Math.round(metrics.dti_ratio * 100) : 0;

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md">
      {/* Card Header Layer */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-4">
        <h3 className="text-lg font-semibold text-slate-800">📋 Application Risk Metrics</h3>
        <span className={`inline-flex items-center rounded-md px-2.5 py-1 text-xs font-medium ring-1 ring-inset ${
          isEscalated 
            ? 'bg-amber-50 text-amber-700 ring-amber-600/10' 
            : status === 'APPROVE' || status === 'SUCCESS'
            ? 'bg-emerald-50 text-emerald-700 ring-emerald-600/10'
            : 'bg-slate-50 text-slate-600 ring-slate-500/10'
        }`}>
          {status}
        </span>
      </div>
      
      {/* Metric Visual Readouts Layer */}
      <div className="mt-4 space-y-3 text-sm text-slate-600">
        <div className="flex justify-between">
          <span className="font-medium">Cleaned Income:</span> 
          <span className="font-mono text-slate-900">රු. {formatCurrency(metrics?.monthly_income)}</span>
        </div>
        
        <div className="flex justify-between">
          <span className="font-medium">DTI Ratio:</span> 
          <span className={`font-bold ${displayDti > 40 ? 'text-rose-600' : 'text-slate-700'}`}>
            {displayDti}%
          </span>
        </div>
        
        <div className="flex justify-between">
          <span className="font-medium">CRIB Score:</span> 
          <span className={`font-bold ${(metrics?.crib_score ?? 0) < 650 ? 'text-rose-600' : 'text-emerald-600'}`}>
            {metrics?.crib_score ?? 'N/A'}
          </span>
        </div>
      </div>
    </div>
  );
}
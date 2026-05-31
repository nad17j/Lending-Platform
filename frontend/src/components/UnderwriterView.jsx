import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

export default function UnderwriterView() {
  const { user, token, logoutUser } = useAuth();
  const [isProcessing, setIsProcessing] = useState(false);
  const [pipelineData, setPipelineData] = useState(null);
  const [errorState, setErrorState] = useState(null);

  // Automatically execute the production pipeline when the view mounts
  useEffect(() => {
    const fetchPipelineTrace = async () => {
      setIsProcessing(true);
      setErrorState(null);
      try {
        const backendUrl = import.meta.env.VITE_BACKEND_API_URL || "http://127.0.0.1:8000";
        const response = await fetch(`${backendUrl}/api/v1/underwrite`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` // Passing the secure asymmetric JWT from context state
          },
          body: JSON.stringify({
            gcs_document_uri: "gs://prod-lending-vault/docs/app_colombo_2026.pdf",
            crib_score: 710,
            existing_debts_lkr: 50000.00
          })
        });

        if (!response.ok) {
          if (response.status === 403) {
            throw new Error("Security clearance validation mismatch: Insufficient role hierarchy.");
          }
          throw new Error("Upstream lending engine structural processing anomaly.");
        }

        const data = await response.json();
        setPipelineData(data);
      } catch (err) {
        setErrorState(err.message);
      } finally {
        setIsProcessing(false);
      }
    };

    if (token) {
      fetchPipelineTrace();
    }
  }, [token]);

  const handleAction = async (decision) => {
    setIsProcessing(true);
    // Simulates sealing the final verified decision transaction via authenticated session audit log
    setTimeout(() => {
      alert(`Action [${decision}] successfully sealed by ${user?.name || 'Underwriter'} and written to the immutable ledger tracking ID: ${pipelineData?.transaction_id || 'N/A'}`);
      setIsProcessing(false);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Top Header Navigation */}
      <nav className="border-b border-slate-200 bg-white px-6 py-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">🏛️</span>
            <span className="text-xl font-bold tracking-tight text-slate-900">Lending Engine Workbench</span>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm font-semibold text-slate-900">{user?.name || 'Active Underwriter'}</p>
              <p className="text-xs font-medium text-amber-700 bg-amber-50 rounded px-1.5 py-0.5 inline-block">
                {user?.role || 'UNDERWRITER_LEVEL_2'}
              </p>
            </div>
            <button onClick={logoutUser} className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 transition hover:bg-slate-50">
              Exit Terminal
            </button>
          </div>
        </div>
      </nav>

      {/* Main Layout Workspace Content Grid */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        
        {/* Error Alert Display Box */}
        {errorState && (
          <div className="mb-6 rounded-xl bg-rose-50 border border-rose-200 p-4 text-sm text-rose-700 font-medium">
            🚨 [CRITICAL TRACE FAILURE] {errorState}
          </div>
        )}

        <div className="mb-6 flex items-center justify-between border-b border-slate-200 pb-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">Active Production Operational Queue</h1>
            <p className="text-sm text-slate-500">
              Transaction ID Under Review:{' '}
              <code className="font-mono bg-slate-200 text-slate-800 px-1 rounded">
                {pipelineData ? pipelineData.transaction_id : 'Processing network payload...'}
              </code>
            </p>
          </div>
          <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ring-1 ring-inset ${
            pipelineData?.status === "AUTO_APPROVED" 
              ? "bg-emerald-50 text-emerald-700 ring-emerald-600/10" 
              : "bg-rose-50 text-rose-700 ring-rose-600/10 animate-pulse"
          }`}>
            {pipelineData ? `⚠️ STATUS: ${pipelineData.status}` : '📡 PIPELINE STREAM ACTIVE'}
          </span>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          {/* Left Panel: Clean Ingestion Data Metrics */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-bold text-slate-900 border-b border-slate-100 pb-3 mb-4">📋 Parsed Inbound Financial Matrix</h3>
            {isProcessing && !pipelineData ? (
              <div className="space-y-4 py-4 animate-pulse">
                <div className="h-4 bg-slate-200 rounded w-1/3"></div>
                <div className="h-4 bg-slate-200 rounded w-1/2"></div>
                <div className="h-4 bg-slate-200 rounded w-2/3"></div>
              </div>
            ) : (
              <dl className="grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-2">
                <div className="sm:col-span-1">
                  <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Linguistic Extraction Context</div>
                  <div className="mt-1 text-sm font-semibold text-slate-800 bg-slate-100 rounded px-2 py-1 inline-block">
                    GCS_DOCUMENT_AI_RESOLVED
                  </div>
                </div>
                <div className="sm:col-span-1">
                  <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Normalized Base Salary</div>
                  <div className="mt-1 text-sm font-bold text-slate-900">
                    රු. {pipelineData?.metrics?.salary_lkr?.toLocaleString(undefined, {minimumFractionDigits: 2}) || '0.00'}
                  </div>
                </div>
                <div className="sm:col-span-1">
                  <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Requested Capital Outlay</div>
                  <div className="mt-1 text-sm font-bold text-slate-900">රු. 2,500,000.00</div>
                </div>
                <div className="sm:col-span-1">
                  <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Calculated DTI Ratio</div>
                  <div className="mt-1 text-sm font-bold text-rose-600">
                    {pipelineData?.metrics?.dti?.toFixed(2) || '0.00'}%
                  </div>
                </div>
              </dl>
            )}
          </div>

          {/* Right Panel: RAG Agent Intelligence Evidence Layer */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-bold text-slate-900 border-b border-slate-100 pb-3 mb-4">🤖 pgvector RAG Compliance Query</h3>
              <div className="rounded-xl bg-slate-900 p-4 font-mono text-xs text-slate-300 leading-relaxed shadow-inner">
                <p className="text-emerald-400 mb-1">// Central Bank of Sri Lanka System Trace Result:</p>
                <p className="text-amber-400 mb-2">
                  [Policy Logic]: {pipelineData?.evaluation_trace?.reason_code || 'Awaiting telemetry...'}
                </p>
                <div className="border-t border-slate-800 pt-2 mt-2 text-slate-400">
                  "{pipelineData?.evaluation_trace?.compliance_proof || 'No active query traces extracted.'}"
                </div>
              </div>
            </div>
            
            {/* System Action Tray */}
            <div className="mt-6 flex justify-end space-x-3 border-t border-slate-100 pt-4">
              <button 
                disabled={isProcessing || !pipelineData} 
                onClick={() => handleAction("DECLINED")}
                className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-bold text-rose-600 transition hover:bg-rose-50 active:bg-rose-100 disabled:opacity-50"
              >
                Reject Underwriting Profile
              </button>
              <button 
                disabled={isProcessing || !pipelineData} 
                onClick={() => handleAction("OVERRIDE_APPROVED")}
                className="rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-slate-800 active:bg-slate-950 shadow-md disabled:opacity-50"
              >
                Execute Signature Override
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
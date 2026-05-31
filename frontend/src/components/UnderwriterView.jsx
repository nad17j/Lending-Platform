import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function UnderwriterView() {
  const { user, token, logoutUser } = useAuth();
  const [isProcessing, setIsProcessing] = useState(false);

  const mockApplicationData = {
    txId: "tx_2026_5f8a2b1c",
    income: "රු. 125,000.00",
    loanRequested: "රු. 2,500,000.00",
    dti: "40.00%",
    crib: 710,
    ragEvidence: "Section 4.2: Credit History. Active CRIB scores between 650 and 715 require a manual multi-signatory override through an accredited Human Underwriter Workbench."
  };

  const handleAction = async (decision) => {
    setIsProcessing(true);
    // In production, this issues an authorized HTTP call containing the JWT header:
    // headers: { "Authorization": `Bearer ${token}` }
    setTimeout(() => {
      alert(`Action [${decision}] successfully sealed by ${user.name} and logged via JWT signatures.`);
      setIsProcessing(false);
    }, 800);
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
              <p className="text-sm font-semibold text-slate-900">{user.name}</p>
              <p className="text-xs font-medium text-amber-700 bg-amber-50 rounded px-1.5 py-0.5 inline-block">{user.role}</p>
            </div>
            <button onClick={logoutUser} className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 transition hover:bg-slate-50">
              Exit Terminal
            </button>
          </div>
        </div>
      </nav>

      {/* Main Layout Workspace Content Grid */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center justify-between border-b border-slate-200 pb-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">Active High-Risk Operational Queue</h1>
            <p className="text-sm text-slate-500">Transaction ID Under Review: <code className="font-mono bg-slate-200 text-slate-800 px-1 rounded">{mockApplicationData.txId}</code></p>
          </div>
          <span className="inline-flex items-center rounded-full bg-rose-50 px-3 py-1 text-xs font-medium text-rose-700 ring-1 ring-inset ring-rose-600/10 animate-pulse">
            ⚠️ ESCALATION LOOP ACTIVE
          </span>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          {/* Left Panel: Clean Ingestion Data Metrics */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-bold text-slate-900 border-b border-slate-100 pb-3 mb-4">📋 Parsed Inbound Financial Matrix</h3>
            <dl className="grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-2">
              <div className="sm:col-span-1">
                <dt className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Linguistic Context</dt>
                <dd className="mt-1 text-sm font-medium text-slate-900">PERMANENT_EMPLOYEE</dd>
              </div>
              <div className="sm:col-span-1">
                <dt className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Verified Monthly Income</dt>
                <dd className="mt-1 text-sm font-bold text-slate-900">{mockApplicationData.income}</dd>
              </div>
              <div className="sm:col-span-1">
                <dt className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Requested Loan Capital</dt>
                <dd className="mt-1 text-sm font-bold text-slate-900">{mockApplicationData.loanRequested}</dd>
              </div>
              <div className="sm:col-span-1">
                <dt className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Calculated DTI Ceiling</dt>
                <dd className="mt-1 text-sm font-bold text-rose-600">{mockApplicationData.dti}</dd>
              </div>
            </dl>
          </div>

          {/* Right Panel: RAG Agent Intelligence Evidence Layer */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-bold text-slate-900 border-b border-slate-100 pb-3 mb-4">🤖 RAG Semantic Pipeline Verification</h3>
              <div className="rounded-xl bg-slate-900 p-4 font-mono text-xs text-slate-300 leading-relaxed shadow-inner">
                <p className="text-emerald-400 mb-1">// Central Bank of Sri Lanka Regulation Match:</p>
                "{mockApplicationData.ragEvidence}"
              </div>
            </div>
            
            {/* System Action Tray */}
            <div className="mt-6 flex justify-end space-x-3 border-t border-slate-100 pt-4">
              <button disabled={isProcessing} onClick={() => handleAction("DECLINED")}
                className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-bold text-rose-600 transition hover:bg-rose-50 active:bg-rose-100 disabled:opacity-50">
                Reject Underwriting Profile
              </button>
              <button disabled={isProcessing} onClick={() => handleAction("OVERRIDE_APPROVED")}
                className="rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-slate-800 active:bg-slate-950 shadow-md disabled:opacity-50">
                Execute Signature Override
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
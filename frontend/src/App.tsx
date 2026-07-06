import { Plus, ArrowUp, Monitor, FileText, Search, Layout, BookOpen, Clock, Settings, Loader2, PieChart as PieChartIcon, BookMarked, CalendarDays, Swords, Network, Clock3, Brain, ShieldCheck, Download, Mic, MicOff, ExternalLink, ChevronDown } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const CustomBookLogo = () => (
  <svg width="36" height="36" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="50" fill="#2CB5E8"/>
    <path d="M15 75C25 70 35 70 50 80V35C35 25 25 25 15 30V75Z" fill="white"/>
    <path d="M85 75C75 70 65 70 50 80V35C65 25 75 25 85 30V75Z" fill="white"/>
    <path d="M50 35V80" stroke="#2CB5E8" strokeWidth="2.5" strokeLinecap="round"/>
    <path d="M22 42C30 38 40 40 46 45" stroke="#2CB5E8" strokeWidth="2" strokeLinecap="round"/>
    <path d="M22 52C30 48 40 50 46 55" stroke="#2CB5E8" strokeWidth="2" strokeLinecap="round"/>
    <path d="M22 62C30 58 40 60 46 65" stroke="#2CB5E8" strokeWidth="2" strokeLinecap="round"/>
    <path d="M78 42C70 38 60 40 54 45" stroke="#2CB5E8" strokeWidth="2" strokeLinecap="round"/>
    <path d="M78 52C70 48 60 50 54 55" stroke="#2CB5E8" strokeWidth="2" strokeLinecap="round"/>
    <path d="M78 62C70 58 60 60 54 65" stroke="#2CB5E8" strokeWidth="2" strokeLinecap="round"/>
    <path d="M10 78C25 73 35 73 50 83C65 73 75 73 90 78" stroke="white" strokeWidth="4" strokeLinecap="round"/>
  </svg>
);

// Mock data for Data Insights
const trendData = [
  { name: 'Jan', AI: 4000, Biotech: 2400, Quantum: 2400 },
  { name: 'Feb', AI: 3000, Biotech: 1398, Quantum: 2210 },
  { name: 'Mar', AI: 2000, Biotech: 9800, Quantum: 2290 },
  { name: 'Apr', AI: 2780, Biotech: 3908, Quantum: 2000 },
  { name: 'May', AI: 1890, Biotech: 4800, Quantum: 2181 },
  { name: 'Jun', AI: 2390, Biotech: 3800, Quantum: 2500 },
];

const distributionData = [
  { name: 'Academic Papers', value: 400 },
  { name: 'News Articles', value: 300 },
  { name: 'Market Reports', value: 300 },
  { name: 'Patents', value: 200 },
];
const COLORS = ['#5E5CE6', '#2CB5E8', '#10B981', '#F59E0B'];
const API = "http://127.0.0.1:8001";

// ── Web Audio API for guaranteed autoplay ──
let audioCtx: AudioContext | null = null;
const getAudioCtx = () => {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
  }
  return audioCtx;
};

export default function App() {
  const [activeTab, setActiveTab] = useState('New Research');
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState<'quick'|'deep'|'insights'>('quick');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [recentSessions, setRecentSessions] = useState<any[]>([]);
  const [libraryDocuments, setLibraryDocuments] = useState<any[]>([]);

  // ── Feature States ──
  const [featureQuery, setFeatureQuery] = useState('');
  const [featureLoading, setFeatureLoading] = useState(false);
  const [featureResult, setFeatureResult] = useState<any>(null);
  const [explainMode, setExplainMode] = useState<'beginner'|'expert'|'eli5'>('beginner');

  // ── Voice Assistant State ──
  const [isListening, setIsListening] = useState(false);
  const [voiceSupported, setVoiceSupported] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      setVoiceSupported(true);
    }
  }, []);

  useEffect(() => {
    if (activeTab === 'Recents' || activeTab === 'Generated Reports') {
      fetch(`${API}/api/research/sessions`)
        .then(res => res.json())
        .then(data => setRecentSessions(Array.isArray(data) ? data : []))
        .catch(console.error);
    }
    if (activeTab === 'Library') {
      fetch(`${API}/api/documents/`)
        .then(res => res.json())
        .then(data => setLibraryDocuments(Array.isArray(data) ? data : []))
        .catch(console.error);
    }
    // Reset feature result when switching tabs
    setFeatureResult(null);
    setFeatureQuery('');
  }, [activeTab]);

  const handleUploadClick = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setQuery((prev) => prev ? prev + `\n[Attached Document: ${file.name}] ` : `[Attached Document: ${file.name}] `);
    }
  };

  // ── Voice Assistant ──
  const handleVoiceToggle = () => {
    if (!voiceSupported) return;
    
    // Permanently unlock AudioContext on click
    const ctx = getAudioCtx();
    if (ctx.state === 'suspended') {
      ctx.resume();
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognitionRef.current = recognition;

    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      setIsListening(false);
      setTimeout(() => handleSubmit(undefined, transcript, true), 300);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    recognition.start();
  };

  // ── Speak result using BACKEND gTTS - Guaranteed Indian Female voice ──
  const speakResult = async (text: string) => {
    if (!text || !text.trim()) return;
    try {
      const cleanText = text.replace(/[*#_\[\]]/g, '').replace(/\s+/g, ' ').trim().substring(0, 400);
      const res = await fetch(`${API}/api/features/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: cleanText })
      });
      if (!res.ok) throw new Error('TTS API failed');
      
      const arrayBuffer = await res.arrayBuffer();
      const ctx = getAudioCtx();
      const audioBuffer = await ctx.decodeAudioData(arrayBuffer);
      const source = ctx.createBufferSource();
      source.buffer = audioBuffer;
      source.connect(ctx.destination);
      source.start(0);
    } catch (e) {
      console.error('TTS error:', e);
    }
  };

  // ── Main Research Submit ──
  const handleSubmit = async (overrideMode?: 'quick'|'deep'|'insights', overrideQuery?: string, isVoiceSubmit: boolean = false) => {
    const currentMode = overrideMode || mode;
    const currentQuery = overrideQuery || query;
    if (currentMode === 'insights') {
      setIsLoading(true);
      setTimeout(() => { setResult({ mode: 'insights', query: currentQuery }); setIsLoading(false); }, 1500);
      return;
    }
    if (!currentQuery) return;
    setIsLoading(true);
    setError('');
    setResult(null);
    setActiveTab('New Research');
    try {
      const endpoint = currentMode === 'deep' ? `${API}/api/research/deep` : `${API}/api/research/quick`;
      const bodyParams = currentMode === 'deep'
        ? { query: currentQuery, depth: 3, include_timeline: true, include_predictions: true, include_fact_check: true }
        : { query: currentQuery, include_web: true, include_wikipedia: true, max_sources: 5 };
      const startRes = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(bodyParams) });
      if (!startRes.ok) throw new Error(`API Error: ${startRes.statusText}`);
      const startData = await startRes.json();
      const sessionId = startData.session_id;
      let isDone = false;
      while (!isDone) {
        await new Promise(resolve => setTimeout(resolve, 3000));
        const statusRes = await fetch(`${API}/api/research/session/${sessionId}`);
        if (statusRes.ok) {
          const statusData = await statusRes.json();
          if (statusData.status === 'done' || statusData.status === 'error') {
            isDone = true;
            setResult(statusData);
            if (statusData.status === 'error') setError('Research task failed on backend.');
            else {
               if (isVoiceSubmit) {
                 const textToSpeak = statusData.summary || statusData.deep_summary || "Research is complete.";
                 speakResult(textToSpeak);
               }
            }
          }
        }
      }
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to connect to backend.');
    } finally {
      setIsLoading(false);
    }
  };

  // ── Feature API Call ──
  const callFeatureAPI = async (endpoint: string, body: object) => {
    if (!featureQuery.trim()) return;
    setFeatureLoading(true);
    setFeatureResult(null);
    try {
      const res = await fetch(`${API}/api/features/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      if (!res.ok) throw new Error('API error');
      const data = await res.json();
      setFeatureResult(data);
    } catch (e: any) {
      setFeatureResult({ error: e.message });
    } finally {
      setFeatureLoading(false);
    }
  };

  // ── Export Handler ──
  const handleExport = async () => {
    if (!result) return;
    try {
      const res = await fetch(`${API}/api/features/export`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: result.query || 'Research Report',
          summary: result.summary || '',
          deep_summary: result.deep_summary || '',
          sources: result.sources || [],
          keywords: result.keywords || [],
          format: 'markdown'
        })
      });
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'research_report.md';
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (e) { console.error(e); }
  };

  const ICON_PROPS = { size: 24, strokeWidth: 2.5 };
  const SMALL_ICON = { size: 20, strokeWidth: 2.5 };

  // ── Shared Feature Input Box ──
  const FeatureInputBox = ({ placeholder, onSubmit }: { placeholder: string, onSubmit: () => void }) => (
    <div style={{ display: 'flex', gap: '12px', marginBottom: '32px', maxWidth: '720px' }}>
      <input
        type="text"
        value={featureQuery}
        onChange={e => setFeatureQuery(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && onSubmit()}
        placeholder={placeholder}
        style={{ flex: 1, padding: '14px 20px', borderRadius: '16px', border: '1px solid #E5E5EA', fontSize: '15px', fontFamily: 'Inter, sans-serif', outline: 'none', background: 'white' }}
      />
      <button
        onClick={onSubmit}
        disabled={featureLoading}
        style={{ padding: '14px 24px', background: '#5E5CE6', color: 'white', border: 'none', borderRadius: '16px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
      >
        {featureLoading ? <Loader2 size={16} className="animate-spin" /> : <ArrowUp size={16} />}
        {featureLoading ? 'Loading...' : 'Go'}
      </button>
    </div>
  );

  return (
    <>
      {/* ─── SIDEBAR ─── */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <CustomBookLogo />
          <span style={{ fontSize: '18px', color: '#111827', fontWeight: '700' }}>ResearchMind</span>
        </div>

        <div className="sidebar-section">Workspace</div>
        <div className={`sidebar-link ${activeTab === 'New Research' ? 'active' : ''}`} onClick={() => { setActiveTab('New Research'); setMode('quick'); setResult(null); setQuery(''); }}>
          <Plus {...ICON_PROPS} /> New Research
        </div>
        <div className={`sidebar-link ${activeTab === 'Recents' ? 'active' : ''}`} onClick={() => setActiveTab('Recents')}>
          <Clock {...ICON_PROPS} /> Recents
        </div>
        <div className={`sidebar-link ${activeTab === 'Library' ? 'active' : ''}`} onClick={() => { setActiveTab('Library'); setMode('quick'); setResult(null); setQuery(''); }}>
          <BookOpen {...ICON_PROPS} /> Library
        </div>

        <div className="sidebar-section">Features</div>
        <div className={`sidebar-link ${activeTab === 'Deep Search' ? 'active' : ''}`} onClick={() => { setMode('deep'); setActiveTab('Deep Search'); setResult(null); setQuery(''); }}>
          <Search {...ICON_PROPS} color={activeTab === 'Deep Search' ? '#5E5CE6' : undefined} /> Deep Search
        </div>
        <div className={`sidebar-link ${activeTab === 'Document Analysis' ? 'active' : ''}`} onClick={() => { handleUploadClick(); setActiveTab('Document Analysis'); setMode('quick'); }}>
          <FileText {...ICON_PROPS} color={activeTab === 'Document Analysis' ? '#5E5CE6' : undefined} /> Document Analysis
        </div>
        <div className={`sidebar-link ${activeTab === 'Data Insights' ? 'active' : ''}`} onClick={() => { setActiveTab('Data Insights'); setMode('insights'); setResult(null); setQuery(''); }}>
          <PieChartIcon {...ICON_PROPS} color={activeTab === 'Data Insights' ? '#10B981' : undefined} /> Data Insights
        </div>
        <div className={`sidebar-link ${activeTab === 'Generated Reports' ? 'active' : ''}`} onClick={() => { setActiveTab('Generated Reports'); setMode('quick'); setResult(null); setQuery(''); }}>
          <Layout {...ICON_PROPS} color={activeTab === 'Generated Reports' ? '#5E5CE6' : undefined} /> Generated Reports
        </div>

        <div className={`sidebar-link ${activeTab === 'Export Center' ? 'active' : ''}`} onClick={() => setActiveTab('Export Center')}>
          <Download {...ICON_PROPS} color={activeTab === 'Export Center' ? '#5E5CE6' : undefined} /> Export Center
        </div>

        <div style={{ marginTop: 'auto', paddingTop: '16px' }}>
          <div className="sidebar-link">
            <Settings {...ICON_PROPS} /> Settings
          </div>
        </div>
      </aside>

      {/* ─── VOICE MODE OVERLAY ─── */}
      {isListening && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(255,255,255,0.95)', zIndex: 9999, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', backdropFilter: 'blur(10px)' }}>
           <div style={{ width: '120px', height: '120px', borderRadius: '50%', background: '#E11D4820', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '32px', animation: 'pulse 1.5s infinite' }}>
              <div style={{ width: '80px', height: '80px', borderRadius: '50%', background: '#E11D48', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 10px 30px rgba(225, 29, 72, 0.4)' }}>
                 <Mic size={40} color="white" />
              </div>
           </div>
           <h2 style={{ fontSize: '32px', color: '#111827', marginBottom: '16px', fontFamily: '"Instrument Serif", serif' }}>Listening to you...</h2>
           <p style={{ color: '#6B7280', fontSize: '18px' }}>Speak your research query clearly.</p>
           <button onClick={() => { recognitionRef.current?.stop(); setIsListening(false); }} style={{ padding: '12px 32px', background: 'white', border: '1px solid #E5E5EA', borderRadius: '30px', marginTop: '40px', cursor: 'pointer', fontSize: '15px', color: '#4B5563', fontWeight: '600', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>Cancel</button>
           <style>{`
             @keyframes pulse {
               0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.4); }
               70% { transform: scale(1.1); box-shadow: 0 0 0 20px rgba(225, 29, 72, 0); }
               100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
             }
           `}</style>
        </div>
      )}

      {/* ─── MAIN AREA ─── */}
      <main className="main-area">
        <header className="top-header"></header>

        {/* ── RECENTS ── */}
        {activeTab === 'Recents' && (
          <div style={{ padding: '40px', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
            <h1 className="hero-title" style={{ textAlign: 'left', marginBottom: '16px', fontSize: '42px' }}>Recent Research</h1>
            <p style={{ color: '#8E8E93', marginBottom: '40px' }}>Your past queries and generated insights.</p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {recentSessions.length === 0 ? (
                <p style={{ color: '#8E8E93' }}>No recent research found. Start a new search!</p>
              ) : recentSessions.map((recent, idx) => (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px', background: 'white', border: '1px solid #E5E5EA', borderRadius: '12px', cursor: 'pointer' }} onClick={() => { setActiveTab('New Research'); setQuery(recent.query); }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: `${recent.mode === 'deep' ? '#5E5CE6' : '#10B981'}15`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <Clock size={20} color={recent.mode === 'deep' ? '#5E5CE6' : '#10B981'} />
                    </div>
                    <div>
                      <h4 style={{ color: '#111827', margin: 0, marginBottom: '4px' }}>"{recent.query}"</h4>
                      <p style={{ color: '#8E8E93', margin: 0, fontSize: '13px' }}>{recent.mode === 'deep' ? 'Deep Search' : 'Quick Research'} • {new Date(recent.created_at).toLocaleString()}</p>
                    </div>
                  </div>
                  <button style={{ padding: '8px 16px', background: '#F3F4F6', border: 'none', borderRadius: '20px', fontWeight: '600', color: '#4B5563', cursor: 'pointer' }}>Re-run</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── LIBRARY ── */}
        {activeTab === 'Library' && (
          <div style={{ padding: '40px', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
            <h1 className="hero-title" style={{ textAlign: 'left', marginBottom: '16px', fontSize: '42px' }}>Your Library</h1>
            <p style={{ color: '#8E8E93', marginBottom: '40px' }}>Saved documents, PDFs, and past research materials.</p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '20px' }}>
              {libraryDocuments.length === 0 ? (
                <p style={{ color: '#8E8E93' }}>No documents uploaded yet.</p>
              ) : libraryDocuments.map((doc, idx) => (
                <div key={idx} style={{ border: '1px solid #E5E5EA', borderRadius: '16px', padding: '20px', background: 'white', display: 'flex', flexDirection: 'column', gap: '12px', cursor: 'pointer', transition: 'box-shadow 0.2s' }} onMouseEnter={e => e.currentTarget.style.boxShadow = '0 10px 30px rgba(0,0,0,0.05)'} onMouseLeave={e => e.currentTarget.style.boxShadow = 'none'}>
                  <BookOpen size={28} color="#5E5CE6" />
                  <h4 style={{ color: '#111827', wordBreak: 'break-word' }}>{doc.filename || 'Unknown Document'}</h4>
                  <p style={{ color: '#8E8E93', fontSize: '13px' }}>Added {new Date(doc.created_at).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── GENERATED REPORTS ── */}
        {activeTab === 'Generated Reports' && (
          <div style={{ padding: '40px', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
            <h1 className="hero-title" style={{ textAlign: 'left', marginBottom: '16px', fontSize: '42px' }}>Generated Reports</h1>
            <p style={{ color: '#8E8E93', marginBottom: '40px' }}>Polished, exported corporate PDFs, Word docs, and Presentations.</p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {recentSessions.filter(s => s.status === 'done').length === 0 ? (
                <p style={{ color: '#8E8E93' }}>No complete research reports generated yet.</p>
              ) : recentSessions.filter(s => s.status === 'done').map((report, idx) => (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px', background: 'white', border: '1px solid #E5E5EA', borderRadius: '12px', cursor: 'pointer' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: '#5E5CE615', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <FileText size={20} color="#5E5CE6" />
                    </div>
                    <div>
                      <h4 style={{ color: '#111827', margin: 0, marginBottom: '4px' }}>{report.query?.substring(0, 40)}... Report</h4>
                      <p style={{ color: '#8E8E93', margin: 0, fontSize: '13px' }}>Research Output • Generated {new Date(report.created_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <button style={{ padding: '8px 16px', background: '#F3F4F6', border: 'none', borderRadius: '20px', fontWeight: '600', color: '#4B5563', cursor: 'pointer' }}>Download PDF</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── EXPORT CENTER ── */}
        {activeTab === 'Export Center' && (
          <div style={{ padding: '40px', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
            <h1 className="hero-title" style={{ textAlign: 'left', marginBottom: '8px', fontSize: '42px' }}>Export Center</h1>
            <p style={{ color: '#8E8E93', marginBottom: '32px' }}>Download your research reports in different formats.</p>
            {result && result.summary ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div style={{ padding: '24px', background: 'white', border: '1px solid #E5E5EA', borderRadius: '16px' }}>
                  <h3 style={{ marginBottom: '8px', color: '#111827' }}>📄 Latest Research Report</h3>
                  <p style={{ color: '#8E8E93', fontSize: '14px', marginBottom: '20px' }}>Query: "{result.query}"</p>
                  <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                    <button onClick={handleExport} style={{ padding: '12px 24px', background: '#5E5CE6', color: 'white', border: 'none', borderRadius: '12px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Download size={16} /> Download Markdown
                    </button>
                    <button onClick={() => { const content = `${result.query}\n\n${result.summary}\n\n${result.deep_summary || ''}`; const blob = new Blob([content], {type:'text/plain'}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href=url; a.download='report.txt'; a.click(); }} style={{ padding: '12px 24px', background: '#F3F4F6', color: '#4B5563', border: 'none', borderRadius: '12px', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <FileText size={16} /> Download TXT
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div style={{ padding: '32px', background: '#F9FAFB', borderRadius: '16px', textAlign: 'center', border: '1px dashed #E5E5EA' }}>
                <Download size={40} color="#D1D5DB" style={{ margin: '0 auto 16px' }} />
                <h3 style={{ color: '#9CA3AF', marginBottom: '8px' }}>No report to export yet</h3>
                <p style={{ color: '#D1D5DB', fontSize: '14px' }}>Run a research query first, then come back here to export it.</p>
              </div>
            )}
          </div>
        )}

        {/* ── MAIN RESEARCH / ALL OTHER TABS ── */}
        {activeTab !== 'Library' && activeTab !== 'Generated Reports' && activeTab !== 'Recents' &&
          activeTab !== 'Export Center' && (
          <div className="hero-container" style={{ justifyContent: result ? 'flex-start' : 'center', marginTop: result ? '0' : '-60px' }}>
            {!result && <h1 className="hero-title">
              {activeTab === 'Deep Search' ? 'Deep Web Analysis' :
               activeTab === 'Document Analysis' ? 'Analyze Your Documents' :
               activeTab === 'Data Insights' ? 'Discover Data Insights' : 'What would you like to research?'}
            </h1>}

            <div className="search-wrapper">
              <div className="search-box" style={{ borderColor: mode === 'deep' ? '#5E5CE6' : mode === 'insights' ? '#10B981' : '#E5E5EA', transition: 'border-color 0.3s' }}>
                <textarea
                  placeholder={mode === 'deep' ? "Enter a complex topic for deep analysis..." : mode === 'insights' ? "Enter a dataset or topic to generate visual insights..." : "Assign a research task or upload a document..."}
                  rows={2}
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(); } }}
                />
                <div className="purple-dot" style={{ background: mode === 'deep' ? '#E11D48' : mode === 'insights' ? '#10B981' : '#5E5CE6' }}></div>

                {/* Upload Button */}
                <button className="upload-btn" title="Import Data/Files" onClick={handleUploadClick} disabled={isLoading}>
                  <Plus size={20} />
                </button>

                {/* Voice Assistant Button */}
                {voiceSupported && (
                  <button
                    title={isListening ? "Stop Listening" : "Voice Search (Indian English)"}
                    onClick={handleVoiceToggle}
                    style={{
                      width: '32px', height: '32px', borderRadius: '50%',
                      background: isListening ? '#E11D48' : '#F2F2F7',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      border: 'none', cursor: 'pointer',
                      position: 'absolute', right: '60px', bottom: '16px',
                      transition: 'all 0.2s',
                      animation: isListening ? 'spin 1s linear infinite' : 'none'
                    }}
                  >
                    {isListening ? <MicOff size={16} color="white" /> : <Mic size={16} color="#8E8E93" />}
                  </button>
                )}

                <input type="file" ref={fileInputRef} style={{ display: 'none' }} accept=".pdf,.docx,.txt,.csv,.xlsx" onChange={handleFileChange} />

                <button className="submit-btn" title={mode === 'deep' ? "Start Deep Research" : mode === 'insights' ? "Generate Insights" : "Start Quick Research"} onClick={() => handleSubmit()} disabled={isLoading}>
                  {isLoading ? <Loader2 size={18} className="animate-spin" /> : <ArrowUp size={18} />}
                </button>
              </div>

              {!result && !isLoading && mode !== 'insights' && (
                <div className="suggestions">
                  <div className="suggestion-pill" onClick={() => handleUploadClick()}><FileText size={16} /> Analyze PDF</div>
                  <div className="suggestion-pill" onClick={() => { setMode('deep'); setQuery("Perform a comprehensive deep web search on Agentic AI"); handleSubmit('deep'); }}><Search size={16} /> Deep Web Search</div>
                  <div className="suggestion-pill" onClick={() => { setActiveTab('Data Insights'); setMode('insights'); setQuery("Generate market share insights for AI tools"); handleSubmit('insights'); }}><Monitor size={16} /> Generate Charts</div>
                </div>
              )}
            </div>

            {/* Loading */}
            {isLoading && (
              <div style={{ marginTop: '40px', textAlign: 'center', color: '#4B5563' }}>
                <Loader2 size={32} className="animate-spin" style={{ margin: '0 auto 16px auto', color: mode === 'insights' ? '#10B981' : '#5E5CE6' }} />
                <h3>{mode === 'deep' ? 'Conducting Deep Research...' : mode === 'insights' ? 'Processing Data & Rendering Charts...' : 'Researching...'}</h3>
                <p>AI agents are gathering and analyzing information across multiple sources.</p>
              </div>
            )}

            {error && (
              <div style={{ marginTop: '40px', padding: '20px', background: '#FEE2E2', color: '#991B1B', borderRadius: '12px', border: '1px solid #F87171' }}>
                <strong>Error:</strong> {error}
              </div>
            )}

            {/* Results */}
            {result && result.mode !== 'insights' && !isLoading && (
              <div style={{ marginTop: '40px', padding: '32px', background: 'white', borderRadius: '24px', border: '1px solid #E5E5EA', width: '100%', maxWidth: '800px', boxShadow: '0 4px 20px rgba(0,0,0,0.03)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
                  <h2 style={{ fontFamily: '"Instrument Serif", serif', fontSize: '32px', margin: 0 }}>
                    {result.mode === 'deep' ? 'Deep Analysis Results' : 'Research Results'}
                  </h2>
                  <div style={{ display: 'flex', gap: '12px' }}>
                    <button onClick={() => speakResult(result.summary || "No summary available")} title="Listen to results" style={{ padding: '8px 16px', background: '#F3F4F6', border: 'none', borderRadius: '20px', fontWeight: '600', color: '#5E5CE6', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px' }}>
                      🔊 Listen (Voice)
                    </button>
                    <button onClick={handleExport} title="Export to Markdown" style={{ padding: '8px 16px', background: '#F3F4F6', border: 'none', borderRadius: '20px', fontWeight: '600', color: '#4B5563', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px' }}>
                      <Download size={14} /> Export
                    </button>
                  </div>
                </div>

                <div style={{ marginBottom: '24px' }}>
                  <h4 style={{ color: '#4B5563', textTransform: 'uppercase', fontSize: '12px', letterSpacing: '1px', marginBottom: '8px' }}>Summary</h4>
                  <p style={{ lineHeight: '1.6', color: '#1A1A1A' }}>{result.summary || "No summary generated."}</p>
                </div>

                {result.mode === 'deep' && result.deep_summary && (
                  <div style={{ marginBottom: '24px', padding: '16px', background: '#F9FAFB', borderRadius: '12px' }}>
                    <h4 style={{ color: '#4B5563', textTransform: 'uppercase', fontSize: '12px', letterSpacing: '1px', marginBottom: '8px' }}>Deep Synthesis</h4>
                    <p style={{ lineHeight: '1.6', color: '#1A1A1A' }}>{result.deep_summary}</p>
                  </div>
                )}

                {result.sources && result.sources.length > 0 && (
                  <div>
                    <h4 style={{ color: '#4B5563', textTransform: 'uppercase', fontSize: '12px', letterSpacing: '1px', marginBottom: '12px' }}>Sources ({result.sources.length})</h4>
                    <ul style={{ listStyleType: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {result.sources.map((src: any, idx: number) => (
                        <li key={idx} style={{ padding: '12px', background: '#F9FAFB', borderRadius: '8px', border: '1px solid #E5E7EB', fontSize: '14px' }}>
                          <a href={src.url} target="_blank" rel="noreferrer" style={{ color: '#5E5CE6', textDecoration: 'none', fontWeight: '500' }}>{src.title || src.url}</a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* Data Insights */}
            {result && result.mode === 'insights' && !isLoading && (
              <div style={{ marginTop: '40px', padding: '32px', background: 'white', borderRadius: '24px', border: '1px solid #E5E5EA', width: '100%', maxWidth: '900px', boxShadow: '0 4px 20px rgba(0,0,0,0.03)' }}>
                <h2 style={{ marginBottom: '24px', fontFamily: '"Instrument Serif", serif', fontSize: '32px' }}>Data Insights & Visualization</h2>
                <p style={{ color: '#4B5563', marginBottom: '32px' }}>Based on your query, we have generated visual models and charts summarizing the data trends.</p>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
                  <div style={{ border: '1px solid #E5E5EA', borderRadius: '16px', padding: '16px' }}>
                    <h4 style={{ color: '#111827', marginBottom: '16px', fontSize: '15px' }}>Sector Growth (Bar)</h4>
                    <ResponsiveContainer width="100%" height={250}>
                      <BarChart data={trendData}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} />
                        <YAxis axisLine={false} tickLine={false} />
                        <Tooltip cursor={{fill: '#F3F4F6'}} />
                        <Legend />
                        <Bar dataKey="AI" fill="#5E5CE6" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Biotech" fill="#2CB5E8" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <div style={{ border: '1px solid #E5E5EA', borderRadius: '16px', padding: '16px' }}>
                    <h4 style={{ color: '#111827', marginBottom: '16px', fontSize: '15px' }}>Source Distribution (Pie)</h4>
                    <ResponsiveContainer width="100%" height={250}>
                      <PieChart>
                        <Pie data={distributionData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                          {distributionData.map((_, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                        </Pie>
                        <Tooltip />
                        <Legend verticalAlign="bottom" height={36} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
                <div style={{ border: '1px solid #E5E5EA', borderRadius: '16px', padding: '16px', marginTop: '32px' }}>
                  <h4 style={{ color: '#111827', marginBottom: '16px', fontSize: '15px' }}>Yearly Trend Analysis (Line)</h4>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={trendData}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="name" axisLine={false} tickLine={false} />
                      <YAxis axisLine={false} tickLine={false} />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="AI" stroke="#5E5CE6" strokeWidth={3} activeDot={{ r: 8 }} />
                      <Line type="monotone" dataKey="Biotech" stroke="#2CB5E8" strokeWidth={3} />
                      <Line type="monotone" dataKey="Quantum" stroke="#10B981" strokeWidth={3} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </>
  );
}

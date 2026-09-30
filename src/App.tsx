import React, { useState, useEffect } from 'react';
import {
  Calculator,
  Grid,
  Divide,
  RotateCcw,
  BookOpen,
  History,
  CheckCircle,
  AlertCircle,
  HelpCircle,
  Sun,
  Moon,
  ArrowRight,
  Plus,
  Minus,
  X,
  Sparkles,
  Trash2,
  Menu,
  Eye,
  RefreshCw,
  Copy
} from 'lucide-react';

type Page = 'home' | 'operations' | 'transpose' | 'determinant' | 'inverse' | 'solver' | 'history' | 'help';

interface HistoryItem {
  id: number;
  date?: string;
  timestamp: string;
  operation: string;
  action_type?: string;
  formula?: string;
  dimensions?: string;
  result_summary?: string;
  matrix_a?: any;
  matrix_b?: any;
  inputs?: any;
  matrices?: any;
  result: any;
  steps: any[];
  solution_type?: string;
}

/**
 * Custom Input Component that auto-clears "0" on focus and resets to "0" on empty blur
 */
function MatrixCellInput({
  value,
  onChange,
  className,
  placeholder = "0"
}: {
  key?: React.Key;
  value: string;
  onChange: (val: string) => void;
  className?: string;
  placeholder?: string;
}) {
  const [focused, setFocused] = useState(false);

  return (
    <input
      type="text"
      value={focused && value === '0' ? '' : value}
      onFocus={(e) => {
        setFocused(true);
        if (value === '0') {
          onChange('');
        } else {
          e.target.select();
        }
      }}
      onBlur={() => {
        setFocused(false);
        if (value.trim() === '') {
          onChange('0');
        }
      }}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className={className}
    />
  );
}

/**
 * Reusable MatrixDisplay component that renders a matrix enclosed in smooth, large curved brackets
 * inside a framed rectangular outer box, exactly like LaTeX / mathematical textbooks as shown in the photo.
 */
function MatrixDisplay({ matrix, title, theme = 'dark' }: { matrix: any[][]; title?: string; theme?: 'dark' | 'light' }) {
  if (!Array.isArray(matrix) || matrix.length === 0) return null;

  return (
    <div className="flex flex-col items-center justify-center my-2">
      {/* Rectangular Box Frame as seen in the photo */}
      <div className={`border-2 rounded-md p-4 shadow-xl inline-flex flex-col items-center min-w-[180px] transition-all ${
        theme === 'dark' ? 'border-slate-700 bg-slate-900/90 text-slate-100' : 'border-slate-800 bg-white text-slate-900'
      }`}>
        {title && (
          <div className="text-[10px] font-bold tracking-widest text-slate-400 mb-2 uppercase text-center border-b border-slate-800 pb-1 w-full">
            {title}
          </div>
        )}

        {/* Outer Flex Container with Left and Right SVG Parentheses */}
        <div className="flex items-stretch gap-2">
          {/* Left Large Parenthesis SVG */}
          <svg className="w-3.5 h-auto text-blue-500 fill-none stroke-current stroke-[2.8]" viewBox="0 0 20 100" preserveAspectRatio="none">
            <path d="M18 2 C 3 20, 3 80, 18 98" strokeLinecap="round" />
          </svg>

          {/* Matrix Columns & Rows */}
          <div className="flex flex-col justify-center gap-2 py-1 px-2">
            {matrix.map((row, rIdx) => (
              <div key={rIdx} className="flex gap-4 justify-center items-center font-mono font-bold text-sm md:text-base">
                {Array.isArray(row) ? (
                  row.map((val, cIdx) => (
                    <span key={cIdx} className="min-w-[28px] text-center tracking-tight text-emerald-400">
                      {String(val)}
                    </span>
                  ))
                ) : (
                  <span className="min-w-[28px] text-center text-emerald-400">{String(row)}</span>
                )}
              </div>
            ))}
          </div>

          {/* Right Large Parenthesis SVG */}
          <svg className="w-3.5 h-auto text-blue-500 fill-none stroke-current stroke-[2.8]" viewBox="0 0 20 100" preserveAspectRatio="none">
            <path d="M2 2 C 17 20, 17 80, 2 98" strokeLinecap="round" />
          </svg>
        </div>
      </div>
    </div>
  );
}

/**
 * Renders the mathematical calculation equation side-by-side in History (Input A [op] Input B = Result)
 */
function HistoryEquationDisplay({ item, theme }: { item: HistoryItem; theme: 'dark' | 'light' }) {
  const { operation, inputs, result } = item;

  // Addition (A + B)
  if (operation.includes('Addition') && inputs?.A && inputs?.B) {
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <MatrixDisplay matrix={inputs.A} title="Matrice A" theme={theme} />
        <span className="text-2xl font-black text-blue-400 font-mono self-center px-1">+</span>
        <MatrixDisplay matrix={inputs.B} title="Matrice B" theme={theme} />
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
        <MatrixDisplay matrix={result} title="Résultat (A + B)" theme={theme} />
      </div>
    );
  }

  // Soustraction (A - B)
  if (operation.includes('Soustraction') && inputs?.A && inputs?.B) {
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <MatrixDisplay matrix={inputs.A} title="Matrice A" theme={theme} />
        <span className="text-2xl font-black text-blue-400 font-mono self-center px-1">−</span>
        <MatrixDisplay matrix={inputs.B} title="Matrice B" theme={theme} />
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
        <MatrixDisplay matrix={result} title="Résultat (A - B)" theme={theme} />
      </div>
    );
  }

  // Multiplication (A × B)
  if (operation.includes('Multiplication') && inputs?.A && inputs?.B) {
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <MatrixDisplay matrix={inputs.A} title="Matrice A" theme={theme} />
        <span className="text-2xl font-black text-blue-400 font-mono self-center px-1">×</span>
        <MatrixDisplay matrix={inputs.B} title="Matrice B" theme={theme} />
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
        <MatrixDisplay matrix={result} title="Résultat (A × B)" theme={theme} />
      </div>
    );
  }

  // Division (A ÷ B)
  if (operation.includes('Division') && inputs?.A && inputs?.B) {
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <MatrixDisplay matrix={inputs.A} title="Matrice A" theme={theme} />
        <span className="text-2xl font-black text-blue-400 font-mono self-center px-1">÷</span>
        <MatrixDisplay matrix={inputs.B} title="Matrice B" theme={theme} />
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
        <MatrixDisplay matrix={result} title="Résultat (A ÷ B)" theme={theme} />
      </div>
    );
  }

  // Transposée (Aᵀ)
  if (operation.includes('Transposée') && inputs?.A) {
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <div className="relative">
          <MatrixDisplay matrix={inputs.A} title="Matrice A" theme={theme} />
          <span className="absolute top-1 right-0 text-sm font-extrabold text-blue-400 font-mono">ᵀ</span>
        </div>
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
        <MatrixDisplay matrix={result} title="Transposée (Aᵀ)" theme={theme} />
      </div>
    );
  }

  // Déterminant Det(A)
  if (operation.includes('Déterminant') && inputs?.A) {
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <div className="flex items-center gap-1">
          <span className="text-base font-bold text-blue-400 font-mono">Det</span>
          <MatrixDisplay matrix={inputs.A} title="Matrice A" theme={theme} />
        </div>
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
        <div className="px-5 py-3 rounded-xl bg-slate-950 text-emerald-400 font-mono text-2xl font-black border border-slate-800 shadow-md">
          {typeof result === 'object' ? JSON.stringify(result) : String(result)}
        </div>
      </div>
    );
  }

  // Matrice Inverse (A⁻¹)
  if (operation.includes('Inverse') && inputs?.A) {
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <div className="relative">
          <MatrixDisplay matrix={inputs.A} title="Matrice A" theme={theme} />
          <span className="absolute top-1 right-0 text-xs font-extrabold text-blue-400 font-mono">⁻¹</span>
        </div>
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
        {Array.isArray(result) ? (
          <MatrixDisplay matrix={result} title="Inverse (A⁻¹)" theme={theme} />
        ) : (
          <span className="px-4 py-2 rounded-lg bg-red-500/10 text-red-400 border border-red-500/30 text-sm font-semibold">
            Non Inversible (Det = 0)
          </span>
        )}
      </div>
    );
  }

  // Matrice Identité (I_n)
  if (operation.includes('Identité')) {
    const dim = inputs?.n || (Array.isArray(result) ? result.length : 3);
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <span className="text-xl font-bold text-blue-400 font-mono">I_{dim} ({dim}×{dim})</span>
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
        <MatrixDisplay matrix={result} title={`Identité I_${dim}`} theme={theme} />
      </div>
    );
  }

  // Système d'équations (AX = B)
  if (operation.includes('Système') && inputs?.A) {
    const vectorB = Array.isArray(inputs.B) ? inputs.B.map((x: any) => [x]) : null;
    return (
      <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
        <MatrixDisplay matrix={inputs.A} title="Matrice A" theme={theme} />
        <span className="text-base font-bold text-blue-400 font-mono">· X =</span>
        {vectorB && <MatrixDisplay matrix={vectorB} title="Vecteur B" theme={theme} />}
        <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">➔</span>
        <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-emerald-400 font-mono font-bold text-sm">
          {typeof result === 'object' ? (
            result.vector ? (
              <div>
                <div className="text-xs text-blue-400 mb-1">Solution ({result.type}) :</div>
                <div>X = [ {result.vector.join(', ')} ]</div>
              </div>
            ) : JSON.stringify(result)
          ) : String(result)}
        </div>
      </div>
    );
  }

  // Fallback default side-by-side
  return (
    <div className="flex flex-wrap items-center justify-center gap-4 py-3 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80 overflow-x-auto">
      {inputs?.A && Array.isArray(inputs.A) && (
        <MatrixDisplay matrix={inputs.A} title="Donnée A" theme={theme} />
      )}
      {inputs?.B && Array.isArray(inputs.B) && (
        <MatrixDisplay matrix={inputs.B} title="Donnée B" theme={theme} />
      )}
      <span className="text-2xl font-black text-emerald-400 font-mono self-center px-1">=</span>
      {Array.isArray(result) ? (
        <MatrixDisplay matrix={result} title="Résultat" theme={theme} />
      ) : (
        <div className="p-3 bg-slate-950 text-emerald-400 font-mono font-bold rounded-lg border border-slate-800">
          {typeof result === 'object' ? JSON.stringify(result) : String(result)}
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home');
  const [opSubTab, setOpSubTab] = useState<'add' | 'subtract' | 'multiply' | 'divide'>('add');
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

  // Splash Screen State (3 seconds load)
  const [showSplash, setShowSplash] = useState<boolean>(true);
  const [splashProgress, setSplashProgress] = useState<number>(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSplashProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 5;
      });
    }, 110);

    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);

    return () => {
      clearInterval(interval);
      clearTimeout(timer);
    };
  }, []);

  // Matrix A state
  const [rowsA, setRowsA] = useState<number>(2);
  const [colsA, setColsA] = useState<number>(2);
  const [gridA, setGridA] = useState<string[][]>([
    ['0', '0'],
    ['0', '0']
  ]);

  // Matrix B state
  const [rowsB, setRowsB] = useState<number>(2);
  const [colsB, setColsB] = useState<number>(2);
  const [gridB, setGridB] = useState<string[][]>([
    ['0', '0'],
    ['0', '0']
  ]);

  // System Solver state
  const [systemSize, setSystemSize] = useState<number>(3);
  const [systemA, setSystemA] = useState<string[][]>([
    ['0', '0', '0'],
    ['0', '0', '0'],
    ['0', '0', '0']
  ]);
  const [systemB, setSystemB] = useState<string[]>(['0', '0', '0']);

  // Results & Loading
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [resultMatrix, setResultMatrix] = useState<any>(null);
  const [resultSingle, setResultSingle] = useState<string | null>(null);
  const [steps, setSteps] = useState<any[]>([]);
  const [solutionType, setSolutionType] = useState<string | null>(null);
  const [solutionVector, setSolutionVector] = useState<string[] | null>(null);
  const [systemExplanation, setSystemExplanation] = useState<string | null>(null);

  // Helper to immediately clear out all calculation results
  const clearResults = () => {
    setErrorMsg(null);
    setResultMatrix(null);
    setResultSingle(null);
    setSteps([]);
    setSolutionType(null);
    setSolutionVector(null);
    setSystemExplanation(null);
  };

  // Reset results immediately whenever the user changes the page or sub-tab
  useEffect(() => {
    clearResults();
  }, [currentPage, opSubTab]);

  // History state & modal state
  const [historyList, setHistoryList] = useState<HistoryItem[]>([]);
  const [selectedHistoryModalItem, setSelectedHistoryModalItem] = useState<HistoryItem | null>(null);
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  // Reload calculation into interface
  const reloadHistoryCalculation = (item: HistoryItem) => {
    const action = item.action_type || (
      item.operation.toLowerCase().includes('addition') ? 'add' :
      item.operation.toLowerCase().includes('soustraction') ? 'subtract' :
      item.operation.toLowerCase().includes('multiplication') ? 'multiply' :
      item.operation.toLowerCase().includes('division') ? 'divide' :
      item.operation.toLowerCase().includes('transpos') ? 'transpose' :
      item.operation.toLowerCase().includes('déterminant') ? 'determinant' :
      item.operation.toLowerCase().includes('inverse') ? 'inverse' :
      item.operation.toLowerCase().includes('système') ? 'solve_system' : 'add'
    );

    const matA = item.matrix_a || item.inputs?.A;
    const matB = item.matrix_b || item.inputs?.B;

    if (action === 'add' || action === 'subtract' || action === 'multiply' || action === 'divide') {
      setCurrentPage('operations');
      setOpSubTab(action as any);
      if (matA && Array.isArray(matA) && matA.length > 0) {
        setRowsA(matA.length);
        setColsA(matA[0].length);
        setGridA(matA.map((r: any) => r.map((c: any) => String(c))));
      }
      if (matB && Array.isArray(matB) && matB.length > 0) {
        setRowsB(matB.length);
        setColsB(matB[0].length);
        setGridB(matB.map((r: any) => r.map((c: any) => String(c))));
      }
    } else if (action === 'transpose' || action === 'determinant' || action === 'inverse') {
      setCurrentPage(action as Page);
      if (matA && Array.isArray(matA) && matA.length > 0) {
        setRowsA(matA.length);
        setColsA(matA[0].length);
        setGridA(matA.map((r: any) => r.map((c: any) => String(c))));
      }
    } else if (action === 'solve_system') {
      setCurrentPage('solver');
      if (matA && Array.isArray(matA) && matA.length > 0) {
        setSystemSize(matA.length);
        setSystemA(matA.map((r: any) => r.map((c: any) => String(c))));
      }
      if (matB && Array.isArray(matB)) {
        setSystemB(matB.map((c: any) => String(c)));
      }
    }

    setToastMsg(`Calcul "${item.operation}" rechargé dans l'interface !`);
    setTimeout(() => setToastMsg(null), 3500);
  };

  const deleteHistoryItem = async (id: number) => {
    try {
      const res = await fetch('/api/matrix/delete-history-item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      });
      const data = await res.json();
      if (data.success) {
        setHistoryList(data.history);
        if (selectedHistoryModalItem?.id === id) {
          setSelectedHistoryModalItem(null);
        }
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Adjust Matrix A Grid when dimensions change
  useEffect(() => {
    const newGrid: string[][] = [];
    for (let i = 0; i < rowsA; i++) {
      const row: string[] = [];
      for (let j = 0; j < colsA; j++) {
        row.push(gridA[i]?.[j] ?? '0');
      }
      newGrid.push(row);
    }
    setGridA(newGrid);
  }, [rowsA, colsA]);

  // Adjust Matrix B Grid when dimensions change
  useEffect(() => {
    const newGrid: string[][] = [];
    for (let i = 0; i < rowsB; i++) {
      const row: string[] = [];
      for (let j = 0; j < colsB; j++) {
        row.push(gridB[i]?.[j] ?? '0');
      }
      newGrid.push(row);
    }
    setGridB(newGrid);
  }, [rowsB, colsB]);

  // Adjust System Solver Grid
  useEffect(() => {
    const newA: string[][] = [];
    const newB: string[] = [];
    for (let i = 0; i < systemSize; i++) {
      const row: string[] = [];
      for (let j = 0; j < systemSize; j++) {
        row.push(systemA[i]?.[j] ?? '0');
      }
      newA.push(row);
      newB.push(systemB[i] ?? '0');
    }
    setSystemA(newA);
    setSystemB(newB);
  }, [systemSize]);

  const loadHistory = async () => {
    try {
      const res = await fetch('/api/matrix/history');
      const data = await res.json();
      if (data.success) {
        setHistoryList(data.history);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (currentPage === 'history') {
      loadHistory();
    }
  }, [currentPage]);

  const handleCellChange = (
    gridSetter: React.Dispatch<React.SetStateAction<string[][]>>,
    r: number,
    c: number,
    val: string
  ) => {
    gridSetter((prev) => {
      const next = prev.map((row) => [...row]);
      next[r][c] = val;
      return next;
    });
  };

  const handleSystemBChange = (index: number, val: string) => {
    setSystemB((prev) => {
      const next = [...prev];
      next[index] = val;
      return next;
    });
  };

  const executeCalculation = async (action: string, payloadAdd: any = {}) => {
    setLoading(true);
    setErrorMsg(null);
    setResultMatrix(null);
    setResultSingle(null);
    setSteps([]);
    setSolutionType(null);
    setSolutionVector(null);
    setSystemExplanation(null);

    // Sanitize matrices: convert empty strings or whitespace-only cells to "0"
    const sanitizeGrid = (data: any) => {
      if (!data) return data;
      if (Array.isArray(data)) {
        return data.map((item: any) => {
          if (Array.isArray(item)) {
            return item.map((val: any) => (!val || String(val).trim() === '' ? '0' : String(val).trim()));
          }
          return (!item || String(item).trim() === '' ? '0' : String(item).trim());
        });
      }
      return data;
    };

    const cleanPayload = { ...payloadAdd };
    if (cleanPayload.A) cleanPayload.A = sanitizeGrid(cleanPayload.A);
    if (cleanPayload.B) cleanPayload.B = sanitizeGrid(cleanPayload.B);

    try {
      const response = await fetch('/api/matrix/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, ...cleanPayload })
      });

      const data = await response.json();
      if (!data.success) {
        setErrorMsg(data.error || 'Une erreur est survenue lors du calcul.');
      } else {
        if (data.is_invertible === false) {
          setErrorMsg('La matrice n\'est pas inversible (son déterminant est nul).');
        }

        if (Array.isArray(data.formatted)) {
          setResultMatrix(data.formatted);
        } else if (Array.isArray(data.formatted_augmented)) {
          setResultMatrix(data.formatted_augmented);
        } else if (Array.isArray(data.result)) {
          setResultMatrix(data.result);
        } else {
          setResultMatrix(null);
        }

        if (typeof data.result === 'number' || (data.result !== undefined && data.result !== null && typeof data.result !== 'object')) {
          setResultSingle(String(data.formatted ?? data.result));
        }

        if (data.steps && Array.isArray(data.steps)) {
          setSteps(data.steps);
        }

        if (data.solution_type) {
          setSolutionType(data.solution_type);
          setSolutionVector(
            Array.isArray(data.formatted_vector)
              ? data.formatted_vector
              : Array.isArray(data.vector)
              ? data.vector
              : null
          );
          setSystemExplanation(data.explanation);
        }
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Erreur de connexion au serveur.');
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = async () => {
    try {
      await fetch('/api/matrix/clear-history', { method: 'POST' });
      setHistoryList([]);
    } catch (e) {
      console.error(e);
    }
  };

  if (showSplash) {
    return (
      <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-slate-950 text-slate-100 select-none overflow-hidden">
        {/* Background glow effects */}
        <div className="absolute w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
        <div className="absolute w-[300px] h-[300px] bg-cyan-500/10 rounded-full blur-2xl pointer-events-none"></div>

        <div className="relative z-10 flex flex-col items-center space-y-6 max-w-sm w-full px-6 text-center">
          {/* Logo Badge */}
          <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-2xl blur opacity-75 animate-pulse"></div>
            <div className="relative w-20 h-20 rounded-2xl bg-slate-900 border border-blue-400/40 flex items-center justify-center text-cyan-400 shadow-2xl">
              <Grid className="w-10 h-10 animate-pulse" />
            </div>
          </div>

          {/* Titles */}
          <div className="space-y-1">
            <h1 className="text-3xl font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-500">
              MATRICAL
            </h1>
            <p className="text-xs font-semibold uppercase tracking-widest text-slate-400">
              Calculatrice & Solveur Matriciel
            </p>
          </div>

          {/* Progress Bar Container */}
          <div className="w-full space-y-2 pt-4">
            <div className="flex justify-between items-center text-xs text-slate-400 font-mono">
              <span className="flex items-center gap-1.5 font-medium">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
                Chargement...
              </span>
              <span className="font-bold text-blue-400">{Math.min(splashProgress, 100)}%</span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-900 border border-slate-800 p-0.5 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-blue-600 via-cyan-400 to-blue-400 transition-all duration-150 ease-out shadow-sm shadow-cyan-500/50"
                style={{ width: `${Math.min(splashProgress, 100)}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen flex ${theme === 'dark' ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-800'}`}>
      {/* Sidebar Navigation */}
      <aside className={`transition-all duration-300 border-r flex flex-col justify-between ${
        isSidebarOpen ? 'w-64 p-4 opacity-100 flex-shrink-0' : 'w-0 p-0 border-0 opacity-0 overflow-hidden pointer-events-none'
      } ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'}`}>
        <div>
          <div className="flex items-center gap-3 px-2 py-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-500 shadow-lg shadow-blue-500/20">
              <Grid className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-bold text-lg tracking-wide text-blue-500">MATRICAL</h1>
              <p className="text-xs text-slate-400">Calculatrice & Solveur</p>
            </div>
          </div>

          <nav className="space-y-1">
            {[
              { id: 'home', label: 'Accueil', icon: Grid },
              { id: 'operations', label: 'Opérations (+, -, ×, ÷)', icon: Calculator },
              { id: 'transpose', label: 'Transposée (Aᵀ)', icon: RefreshCw },
              { id: 'determinant', label: 'Déterminant Det(A)', icon: Divide },
              { id: 'inverse', label: 'Matrice Inverse A⁻¹', icon: RotateCcw },
              { id: 'solver', label: 'Système d\'Équations', icon: BookOpen },
              { id: 'history', label: 'Historique', icon: History },
              { id: 'help', label: 'Aide & Théorie', icon: HelpCircle }
            ].map((item) => {
              const Icon = item.icon;
              const active = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentPage(item.id as Page)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    active
                      ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
                      : theme === 'dark'
                      ? 'text-slate-300 hover:bg-slate-800 hover:text-white'
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Theme selector */}
        <div className={`pt-4 border-t ${theme === 'dark' ? 'border-slate-800' : 'border-slate-200'}`}>
          <div className="flex items-center justify-between px-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Thème UI</span>
            <button
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className={`p-2 rounded-lg transition-colors ${
                theme === 'dark' ? 'bg-slate-800 text-yellow-400 hover:bg-slate-700' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </aside>

      {/* Main Workspace */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8 flex flex-col">
        {/* Top Header Navbar with 3-bar Hamburger Menu Button */}
        <header className="flex items-center justify-between mb-6 pb-4 border-b border-slate-800/60">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              title={isSidebarOpen ? "Masquer le menu des opérations" : "Afficher le menu des opérations"}
              className={`p-2.5 rounded-xl border flex items-center justify-center transition-all shadow-md ${
                theme === 'dark'
                  ? 'bg-slate-900 border-slate-800 text-slate-200 hover:bg-slate-800 hover:text-white hover:border-blue-500/50'
                  : 'bg-white border-slate-300 text-slate-700 hover:bg-slate-100 hover:text-slate-900 hover:border-blue-500/50'
              }`}
            >
              <Menu className="w-5 h-5 text-blue-500" />
            </button>

            <div className="flex items-center gap-2">
              {!isSidebarOpen && (
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-500 shadow-sm">
                    <Grid className="w-4 h-4" />
                  </div>
                  <span className="font-bold text-base text-blue-500 tracking-wide">MATRICAL</span>
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className={`p-2 rounded-lg transition-colors ${
                theme === 'dark' ? 'bg-slate-800 text-yellow-400 hover:bg-slate-700' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>
        </header>
        {/* PAGE: HOME */}
        {currentPage === 'home' && (
          <div className="max-w-4xl mx-auto space-y-8 text-center">
            <div className="space-y-3 flex flex-col items-center justify-center text-center">
              <h2 className="text-4xl font-black tracking-tight text-blue-500 text-center">MATRICAL</h2>
              <p className="text-xl font-bold text-slate-300 text-center max-w-2xl">
                Calculatrice matricielle & solveur de systèmes d'équations étape par étape
              </p>
              <p className={`text-sm text-center max-w-2xl leading-relaxed ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>
                Effectuez des opérations matricielles avancées, découvrez la résolution étape par étape et visualisez les algorithmes manuels.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { title: 'Addition & Soustraction', desc: 'Additionnez ou soustrayez deux matrices de mêmes dimensions.', page: 'operations', tab: 'add' },
                { title: 'Multiplication & Divisions', desc: 'Multipliez (A×B) ou divisez (A÷B = A×B⁻¹) deux matrices.', page: 'operations', tab: 'multiply' },
                { title: 'Transposée (Aᵀ)', desc: 'Intervertissez les lignes et colonnes d\'une matrice.', page: 'transpose' },
                { title: 'Déterminant', desc: 'Calculez le déterminant d\'une matrice carrée par élimination.', page: 'determinant' },
                { title: 'Matrice Inverse', desc: 'Calculez A⁻¹ par la méthode de Gauss-Jordan [A|I].', page: 'inverse' },
                { title: 'Système d\'Équations', desc: 'Résolvez AX = B et détectez le type de solution.', page: 'solver' },
                { title: 'Aide & Théorie', desc: 'Consultez les définitions mathématiques et algorithmes.', page: 'help' }
              ].map((item, idx) => (
                <div
                  key={idx}
                  onClick={() => {
                    if (item.tab) setOpSubTab(item.tab as any);
                    setCurrentPage(item.page as Page);
                  }}
                  className={`p-6 rounded-xl border text-center flex flex-col items-center justify-between hover:border-blue-500 hover:shadow-lg hover:shadow-blue-500/10 transition-all cursor-pointer group ${
                    theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'
                  }`}
                >
                  <div className="space-y-2 flex flex-col items-center">
                    <h3 className="font-bold text-lg group-hover:text-blue-400 transition-colors">{item.title}</h3>
                    <p className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}`}>{item.desc}</p>
                  </div>
                  <div className="mt-4 inline-flex items-center gap-1.5 text-xs font-semibold text-blue-500 group-hover:gap-2.5 transition-all">
                    Accéder <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* PAGE: OPERATIONS */}
        {currentPage === 'operations' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold">Opérations Matricielles</h2>

            {/* Sub Tabs */}
            <div className={`flex p-1 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-slate-100 border-slate-200'}`}>
              {[
                { id: 'add', label: 'Addition (A+B)' },
                { id: 'subtract', label: 'Soustraction (A-B)' },
                { id: 'multiply', label: 'Multiplication (A×B)' },
                { id: 'divide', label: 'Divisions (A÷B)' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setOpSubTab(tab.id as any)}
                  className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-colors ${
                    opSubTab === tab.id
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Matrix Inputs */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Matrix A */}
              <div className={`p-5 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-base text-blue-400">Matrice A</h3>
                  <div className="flex items-center gap-2 text-xs">
                    <label>Lignes:</label>
                    <select
                      value={rowsA}
                      onChange={(e) => setRowsA(Number(e.target.value))}
                      className={`p-1 rounded border text-xs ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-300'}`}
                    >
                      {[1, 2, 3, 4, 5].map((n) => (
                        <option key={n} value={n}>{n}</option>
                      ))}
                    </select>
                    <label>Colonnes:</label>
                    <select
                      value={colsA}
                      onChange={(e) => setColsA(Number(e.target.value))}
                      className={`p-1 rounded border text-xs ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-300'}`}
                    >
                      {[1, 2, 3, 4, 5].map((n) => (
                        <option key={n} value={n}>{n}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${colsA}, minmax(0, 1fr))` }}>
                  {gridA.map((row, r) =>
                    row.map((val, c) => (
                      <MatrixCellInput
                        key={`a-${r}-${c}`}
                        value={val}
                        onChange={(v) => handleCellChange(setGridA, r, c, v)}
                        className={`p-2 text-center text-sm font-mono rounded border ${
                          theme === 'dark'
                            ? 'bg-slate-800 border-slate-700 text-white focus:border-blue-500'
                            : 'bg-slate-50 border-slate-300 text-slate-800 focus:border-blue-500'
                        }`}
                      />
                    ))
                  )}
                </div>
              </div>

              {/* Matrix B */}
              <div className={`p-5 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-base text-blue-400">Matrice B</h3>
                  <div className="flex items-center gap-2 text-xs">
                    <label>Lignes:</label>
                    <select
                      value={rowsB}
                      onChange={(e) => setRowsB(Number(e.target.value))}
                      className={`p-1 rounded border text-xs ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-300'}`}
                    >
                      {[1, 2, 3, 4, 5].map((n) => (
                        <option key={n} value={n}>{n}</option>
                      ))}
                    </select>
                    <label>Colonnes:</label>
                    <select
                      value={colsB}
                      onChange={(e) => setColsB(Number(e.target.value))}
                      className={`p-1 rounded border text-xs ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-300'}`}
                    >
                      {[1, 2, 3, 4, 5].map((n) => (
                        <option key={n} value={n}>{n}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${colsB}, minmax(0, 1fr))` }}>
                  {gridB.map((row, r) =>
                    row.map((val, c) => (
                      <MatrixCellInput
                        key={`b-${r}-${c}`}
                        value={val}
                        onChange={(v) => handleCellChange(setGridB, r, c, v)}
                        className={`p-2 text-center text-sm font-mono rounded border ${
                          theme === 'dark'
                            ? 'bg-slate-800 border-slate-700 text-white focus:border-blue-500'
                            : 'bg-slate-50 border-slate-300 text-slate-800 focus:border-blue-500'
                        }`}
                      />
                    ))
                  )}
                </div>
              </div>
            </div>

            {/* Submit Action */}
            <button
              disabled={loading}
              onClick={() => {
                if (opSubTab === 'add') executeCalculation('add', { A: gridA, B: gridB });
                else if (opSubTab === 'subtract') executeCalculation('subtract', { A: gridA, B: gridB });
                else if (opSubTab === 'multiply') executeCalculation('multiply', { A: gridA, B: gridB });
                else executeCalculation('divide', { A: gridA, B: gridB });
              }}
              className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30 transition-colors"
            >
              {loading ? 'Calcul en cours...' : 'Exécuter le calcul'}
            </button>

            {/* Error Display */}
            {errorMsg && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-500 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <p className="text-sm font-medium">{errorMsg}</p>
              </div>
            )}

            {/* Result Display */}
            {Array.isArray(resultMatrix) && (
              <div className={`p-6 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                <h3 className="text-lg font-bold text-emerald-500 mb-4 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5" /> Résultat de la matrice
                </h3>

                <MatrixDisplay matrix={resultMatrix} title="Matrice Résultat" theme={theme} />

                {steps.length > 0 && (
                  <div className="space-y-2 mt-4">
                    <h4 className="font-semibold text-sm">Étapes détaillées du calcul :</h4>
                    <div className="p-4 rounded-lg bg-slate-950 font-mono text-xs text-slate-300 border border-slate-800 max-h-60 overflow-y-auto space-y-1">
                      {steps.map((st: string, idx: number) => (
                        <div key={idx} className="whitespace-pre-wrap">{st}</div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* PAGE: TRANSPOSE */}
        {currentPage === 'transpose' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold">Calcul de la Transposée (Aᵀ)</h2>

            {/* Matrix A Input */}
            <div className={`p-5 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-base text-blue-400">Matrice A</h3>
                <div className="flex items-center gap-2 text-xs">
                  <label>Lignes:</label>
                  <select
                    value={rowsA}
                    onChange={(e) => setRowsA(Number(e.target.value))}
                    className={`p-1 rounded border text-xs ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-300'}`}
                  >
                    {[1, 2, 3, 4, 5].map((n) => (
                      <option key={n} value={n}>{n}</option>
                    ))}
                  </select>
                  <label>Colonnes:</label>
                  <select
                    value={colsA}
                    onChange={(e) => setColsA(Number(e.target.value))}
                    className={`p-1 rounded border text-xs ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-300'}`}
                  >
                    {[1, 2, 3, 4, 5].map((n) => (
                      <option key={n} value={n}>{n}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${colsA}, minmax(0, 1fr))` }}>
                {gridA.map((row, r) =>
                  row.map((val, c) => (
                    <MatrixCellInput
                      key={`a-${r}-${c}`}
                      value={val}
                      onChange={(v) => handleCellChange(setGridA, r, c, v)}
                      className={`p-2 text-center text-sm font-mono rounded border ${
                        theme === 'dark'
                          ? 'bg-slate-800 border-slate-700 text-white focus:border-blue-500'
                          : 'bg-slate-50 border-slate-300 text-slate-800 focus:border-blue-500'
                      }`}
                    />
                  ))
                )}
              </div>
            </div>

            <button
              disabled={loading}
              onClick={() => executeCalculation('transpose', { A: gridA })}
              className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30 transition-colors"
            >
              {loading ? 'Calcul en cours...' : 'Calculer la Transposée Aᵀ'}
            </button>

            {/* Error Display */}
            {errorMsg && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-500 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <p className="text-sm font-medium">{errorMsg}</p>
              </div>
            )}

            {/* Result Display */}
            {Array.isArray(resultMatrix) && (
              <div className={`p-6 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                <h3 className="text-lg font-bold text-emerald-500 mb-4 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5" /> Matrice Transposée (Aᵀ)
                </h3>

                <MatrixDisplay matrix={resultMatrix} title="Transposée Aᵀ" theme={theme} />

                {steps.length > 0 && (
                  <div className="space-y-2 mt-4">
                    <h4 className="font-semibold text-sm">Étapes détaillées du calcul :</h4>
                    <div className="p-4 rounded-lg bg-slate-950 font-mono text-xs text-slate-300 border border-slate-800 max-h-60 overflow-y-auto space-y-1">
                      {steps.map((st: string, idx: number) => (
                        <div key={idx} className="whitespace-pre-wrap">{st}</div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* PAGE: DETERMINANT & INVERSE */}
        {(currentPage === 'determinant' || currentPage === 'inverse') && (
          <div className="max-w-4xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold">
              {currentPage === 'determinant' && 'Calcul du Déterminant Det(A)'}
              {currentPage === 'inverse' && 'Calcul de la Matrice Inverse A⁻¹'}
            </h2>

            {/* Matrix Input */}
            <div className={`p-5 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-base text-blue-400">
                  Matrice A
                </h3>
                <div className="flex items-center gap-2 text-xs">
                  <label>Taille (n×n):</label>
                  <select
                    value={rowsA}
                    onChange={(e) => {
                      const val = Number(e.target.value);
                      setRowsA(val);
                      setColsA(val);
                    }}
                    className={`p-1 rounded border text-xs ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-300'}`}
                  >
                    {[1, 2, 3, 4, 5].map((n) => (
                      <option key={n} value={n}>{n} × {n}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${colsA}, minmax(0, 1fr))` }}>
                {gridA.map((row, r) =>
                  row.map((val, c) => (
                    <MatrixCellInput
                      key={`a-${r}-${c}`}
                      value={val}
                      onChange={(v) => handleCellChange(setGridA, r, c, v)}
                      className={`p-2 text-center text-sm font-mono rounded border ${
                        theme === 'dark'
                          ? 'bg-slate-800 border-slate-700 text-white focus:border-blue-500'
                          : 'bg-slate-50 border-slate-300 text-slate-800 focus:border-blue-500'
                      }`}
                    />
                  ))
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <button
              disabled={loading}
              onClick={() => {
                if (currentPage === 'determinant') executeCalculation('determinant', { A: gridA });
                else executeCalculation('inverse', { A: gridA });
              }}
              className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30 transition-colors"
            >
              {loading ? 'Calcul en cours...' : (
                currentPage === 'determinant' ? 'Calculer le Déterminant Det(A)' : 'Calculer l\'Inverse A⁻¹'
              )}
            </button>

            {/* Error Display */}
            {errorMsg && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-500 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <p className="text-sm font-medium">{errorMsg}</p>
              </div>
            )}

            {/* Single Value Output (Determinant) */}
            {resultSingle !== null && (
              <div className={`p-6 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                <h3 className="text-lg font-bold text-emerald-500 mb-2">Déterminant Détecté</h3>
                <div className="text-2xl font-extrabold text-white mb-6">Det(A) = {resultSingle}</div>

                {steps.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Étapes détaillées :</h4>
                    <div className="p-4 rounded-lg bg-slate-950 font-mono text-xs text-slate-300 border border-slate-800 max-h-60 overflow-y-auto space-y-1">
                      {steps.map((st: string, idx: number) => (
                        <div key={idx} className="whitespace-pre-wrap">{st}</div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Matrix Output (Inverse) or Pedagogical Steps */}
            {(Array.isArray(resultMatrix) || (steps.length > 0 && currentPage === 'inverse')) && (
              <div className={`p-6 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                {Array.isArray(resultMatrix) ? (
                  <>
                    <h3 className="text-lg font-bold text-emerald-500 mb-4 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5" /> Matrice Résultante
                    </h3>
                    <MatrixDisplay matrix={resultMatrix} title="Matrice Résultat" theme={theme} />
                  </>
                ) : (
                  <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 mb-4 flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold text-sm">Matrice Non Inversible</h4>
                      <p className="text-xs text-amber-300/90 mt-0.5">
                        Le déterminant de cette matrice est nul (det(A) = 0). Aucun pivot non nul ne peut être trouvé, l'inversion est donc impossible.
                      </p>
                    </div>
                  </div>
                )}

                {steps.length > 0 && (
                  <div className="space-y-3 mt-6">
                    <div className="flex items-center justify-between">
                      <h4 className="font-bold text-sm text-blue-400 flex items-center gap-2">
                        <span>Explication pédagogique et étapes détaillées :</span>
                      </h4>
                      <button
                        onClick={() => {
                          const text = steps.map((s: any) => typeof s === 'string' ? s : `${s.operation}\n${s.description}`).join('\n\n');
                          navigator.clipboard.writeText(text);
                          alert('Étapes copiées dans le presse-papier !');
                        }}
                        className={`text-xs px-3 py-1 rounded border transition-colors flex items-center gap-1.5 ${
                          theme === 'dark'
                            ? 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'
                            : 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'
                        }`}
                      >
                        <Copy className="w-3.5 h-3.5" />
                        <span>Copier les étapes</span>
                      </button>
                    </div>

                    <div className="p-4 rounded-xl bg-slate-950 font-mono text-xs sm:text-[13px] text-slate-200 border border-slate-800 max-h-[650px] overflow-y-auto space-y-4 leading-relaxed">
                      {steps.map((st: any, idx: number) => (
                        <div key={idx} className="pb-3 border-b border-slate-800/80 last:border-b-0 last:pb-0">
                          {typeof st === 'string' ? (
                            <div className="whitespace-pre-wrap">{st}</div>
                          ) : (
                            <div>
                              <span className="text-blue-400 font-bold">Étape {st.step || idx + 1} : {st.operation}</span>
                              <p className="text-slate-400 text-xs mt-0.5">{st.description}</p>
                              {st.formatted && <div className="text-emerald-400 font-mono mt-1 whitespace-pre-wrap">{st.formatted}</div>}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* PAGE: SYSTEM SOLVER */}
        {currentPage === 'solver' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold">Solveur de Systèmes d'Équations AX = B</h2>

            <div className={`p-5 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-base text-blue-400">Dimension du système</h3>
                <div className="flex items-center gap-2 text-xs">
                  <label>Nombre d'inconnues:</label>
                  <select
                    value={systemSize}
                    onChange={(e) => setSystemSize(Number(e.target.value))}
                    className={`p-1 rounded border text-xs ${theme === 'dark' ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-300'}`}
                  >
                    {[2, 3, 4, 5].map((n) => (
                      <option key={n} value={n}>{n} équations</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="space-y-3">
                {systemA.map((row, r) => (
                  <div key={r} className="flex items-center gap-2 font-mono text-sm">
                    <span className="text-slate-400 w-12 font-bold">Éq {r + 1}:</span>
                    {row.map((val, c) => (
                      <React.Fragment key={c}>
                        <MatrixCellInput
                          value={val}
                          onChange={(v) => handleCellChange(setSystemA, r, c, v)}
                          className={`w-14 p-2 text-center rounded border ${
                            theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white focus:border-blue-500' : 'bg-slate-50 border-slate-300 text-slate-800 focus:border-blue-500'
                          }`}
                        />
                        <span className="text-slate-400 font-semibold">
                          {['x', 'y', 'z', 't', 'w'][c]} {c < systemSize - 1 ? '+' : '='}
                        </span>
                      </React.Fragment>
                    ))}
                    <MatrixCellInput
                      value={systemB[r] ?? '0'}
                      onChange={(v) => handleSystemBChange(r, v)}
                      className={`w-16 p-2 text-center rounded border ${
                        theme === 'dark' ? 'bg-slate-800 border-slate-700 text-emerald-400 font-bold focus:border-blue-500' : 'bg-slate-50 border-slate-300 text-emerald-600 font-bold focus:border-blue-500'
                      }`}
                    />
                  </div>
                ))}
              </div>
            </div>

            <button
              disabled={loading}
              onClick={() => executeCalculation('solve_system', { A: systemA, B: systemB })}
              className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30"
            >
              {loading ? 'Résolution en cours...' : 'Résoudre le système par Gauss-Jordan'}
            </button>

            {/* Error Display */}
            {errorMsg && (
              <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-500 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <p className="text-sm font-medium">{errorMsg}</p>
              </div>
            )}

            {/* Solution Display */}
            {systemExplanation && (
              <div className={`p-6 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}>
                <h3 className="text-lg font-bold mb-2">Analyse de la Solution</h3>
                <p
                  className={`text-base font-bold mb-4 ${
                    solutionType === 'UNIQUE'
                      ? 'text-emerald-500'
                      : solutionType === 'INFINITE'
                      ? 'text-amber-500'
                      : 'text-red-500'
                  }`}
                >
                  {systemExplanation}
                </p>

                {solutionType === 'UNIQUE' && Array.isArray(solutionVector) && (
                  <div className="flex gap-4 p-4 rounded-lg bg-slate-950 border border-slate-800 mb-6">
                    {solutionVector.map((val: string, idx: number) => (
                      <div key={idx} className="text-emerald-400 font-mono font-bold text-lg">
                        {['x', 'y', 'z', 't', 'w'][idx]} = {val}
                      </div>
                    ))}
                  </div>
                )}

                {steps.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm">Étapes de la matrice augmentée [A | B] :</h4>
                    <div className="p-4 rounded-lg bg-slate-950 font-mono text-xs text-slate-300 border border-slate-800 max-h-60 overflow-y-auto space-y-3">
                      {steps.map((st: any, idx: number) => (
                        <div key={idx} className="border-b border-slate-800 pb-2">
                          <div className="text-blue-400 font-bold">Étape {st.step} : {st.operation}</div>
                          <div className="text-slate-400 text-xs mb-1">{st.description}</div>
                          {st.formatted && <div className="text-emerald-400 whitespace-pre">{st.formatted}</div>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* PAGE: HISTORY */}
        {currentPage === 'history' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Historique Complet des Calculs</h2>
                <p className="text-xs text-slate-400">Conservez, révisez et reprenez tous vos calculs matriciels.</p>
              </div>
              {historyList.length > 0 && (
                <button
                  onClick={clearHistory}
                  className="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/30 transition-all"
                >
                  <Trash2 className="w-3.5 h-3.5" /> Effacer tout l'historique
                </button>
              )}
            </div>

            {historyList.length === 0 ? (
              <div className={`p-12 text-center rounded-2xl border ${theme === 'dark' ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200'}`}>
                <History className="w-12 h-12 text-slate-500 mx-auto mb-3 opacity-50" />
                <p className="text-slate-400 font-medium text-sm">Aucun calcul enregistré pour le moment.</p>
                <p className="text-slate-500 text-xs mt-1">Exécutez un calcul pour le retrouver ici avec toutes ses étapes.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {historyList.map((item) => (
                  <div
                    key={item.id}
                    className={`p-5 rounded-2xl border flex flex-col justify-between transition-all ${
                      theme === 'dark' ? 'bg-slate-900/90 border-slate-800 shadow-lg hover:border-slate-700' : 'bg-white border-slate-200 shadow-sm hover:shadow-md'
                    }`}
                  >
                    <div>
                      {/* Title & Date */}
                      <div className="flex items-start justify-between gap-2 mb-3">
                        <div>
                          <h3 className="font-bold text-base text-blue-400 flex items-center gap-1.5">
                            {item.operation}
                            {item.formula && (
                              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                {item.formula}
                              </span>
                            )}
                          </h3>
                          <p className="text-[11px] text-slate-400 font-mono mt-0.5">
                            📅 {item.date || item.timestamp}
                          </p>
                        </div>
                      </div>

                      {/* Dimensions Tag */}
                      {item.dimensions && (
                        <div className="text-xs font-mono font-medium px-2.5 py-1.5 rounded-lg bg-slate-950/80 text-slate-300 border border-slate-800 mb-3 flex items-center gap-2">
                          <span className="text-blue-400 font-bold">Dim :</span> {item.dimensions}
                        </div>
                      )}

                      {/* Result summary block */}
                      <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 mb-4 flex items-center justify-between">
                        <span className="text-[11px] uppercase font-bold text-slate-400 tracking-wider">Résultat :</span>
                        <span className="text-xs font-mono font-bold text-emerald-400 truncate max-w-[180px]">
                          {item.result_summary || (Array.isArray(item.result) ? `Matrice ${item.result.length}×${item.result[0]?.length || 1}` : String(item.result))}
                        </span>
                      </div>
                    </div>

                    {/* Action buttons: [Voir le calcul complet] [Reprendre ce calcul] [Supprimer] */}
                    <div className="flex items-center gap-1.5 pt-3 border-t border-slate-800/80">
                      <button
                        onClick={() => setSelectedHistoryModalItem(item)}
                        className="flex-1 px-2.5 py-2 text-xs font-bold rounded-lg bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center gap-1 shadow-md shadow-blue-600/20 transition-all"
                      >
                        <Eye className="w-3.5 h-3.5" /> Voir complet
                      </button>

                      <button
                        onClick={() => reloadHistoryCalculation(item)}
                        className="flex-1 px-2.5 py-2 text-xs font-bold rounded-lg bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-400 border border-emerald-500/30 flex items-center justify-center gap-1 transition-all"
                      >
                        <RefreshCw className="w-3.5 h-3.5" /> Reprendre
                      </button>

                      <button
                        onClick={() => deleteHistoryItem(item.id)}
                        className="p-2 text-xs font-semibold rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 flex items-center justify-center transition-all"
                        title="Supprimer de l'historique"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* PAGE: HELP */}
        {currentPage === 'help' && (
          <div className="max-w-4xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold">Guide Pédagogique & Aide Théorique</h2>

            {/* Elementary Row Operations Spotlight */}
            <div className={`p-6 rounded-xl border ${theme === 'dark' ? 'bg-blue-950/30 border-blue-800/60' : 'bg-blue-50/70 border-blue-200 shadow-sm'}`}>
              <div className="flex items-center gap-2 mb-3">
                <span className="px-2.5 py-1 rounded-md text-xs font-bold uppercase tracking-wider bg-blue-500/20 text-blue-400 border border-blue-500/30">
                  Théorème Fondamental
                </span>
                <h3 className="text-lg font-bold text-blue-400">Les 3 opérations élémentaires autorisées sur les lignes</h3>
              </div>
              <p className={`text-sm mb-4 ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                Toute résolution de système linéaire (Gauss), inversion de matrice (Gauss-Jordan) et triangularisation pour le calcul de déterminant repose exclusivement sur ces 3 transformations réversibles sur les lignes L₁, L₂, ... :
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className={`p-4 rounded-lg border font-mono ${theme === 'dark' ? 'bg-slate-900/90 border-slate-800' : 'bg-white border-slate-200'}`}>
                  <div className="text-emerald-400 font-bold text-sm mb-1">1. L_i ← c · L_i</div>
                  <div className="text-xs text-slate-400">
                    Multiplier une ligne L_i par un scalaire non nul <span className="font-semibold text-slate-200">c ≠ 0</span> (ex: normaliser un pivot à 1).
                  </div>
                </div>

                <div className={`p-4 rounded-lg border font-mono ${theme === 'dark' ? 'bg-slate-900/90 border-slate-800' : 'bg-white border-slate-200'}`}>
                  <div className="text-blue-400 font-bold text-sm mb-1">2. L_i ← L_i + c · L_j</div>
                  <div className="text-xs text-slate-400">
                    Ajouter à une ligne L_i le multiple d'une autre ligne L_j (<span className="font-semibold text-slate-200">j ≠ i</span>) pour annuler un coefficient.
                  </div>
                </div>

                <div className={`p-4 rounded-lg border font-mono ${theme === 'dark' ? 'bg-slate-900/90 border-slate-800' : 'bg-white border-slate-200'}`}>
                  <div className="text-amber-400 font-bold text-sm mb-1">3. L_i ↔ L_j</div>
                  <div className="text-xs text-slate-400">
                    Échanger deux lignes distinctes pour positionner un pivot non nul au bon emplacement.
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              {[
                {
                  title: "1. Qu'est-ce qu'une matrice ?",
                  content: "Une matrice m × n est un tableau de nombres ordonnés en m lignes (notées L₁, L₂, ...) et n colonnes (notées C₁, C₂, ...)."
                },
                {
                  title: "2. Matrice Identité Iₙ (L'équivalent du chiffre 1)",
                  content: "Pour les matrices, l'identité Iₙ joue le même rôle que le chiffre 1 pour les nombres (A × Iₙ = A). Sur chaque ligne L_i, il y a un 1 en colonne i et 0 partout ailleurs (L₁ = [1, 0, 0], L₂ = [0, 1, 0], L₃ = [0, 0, 1]). Multiplier une ligne par Iₙ redonne la ligne sans la changer (1·L₁ + 0·L₂ = L₁). C'est la matrice cible obtenue par les 3 opérations élémentaires avec Gauss-Jordan."
                },
                {
                  title: "3. Addition et Soustraction",
                  content: "Nécessite que les deux matrices aient exactement les mêmes dimensions. Calcul élément par élément C[i][j] = A[i][j] ± B[i][j]."
                },
                {
                  title: "4. Multiplication Matricielle",
                  content: "Possible uniquement si le nombre de colonnes de A égale le nombre de lignes de B. Formule : C[i][j] = Σ A[i][k] * B[k][j]."
                },
                {
                  title: "5. Déterminant Det(A)",
                  content: "Valeur scalaire associée à une matrice carrée. Calculée par triangularisation de Gauss avec les opérations sur les lignes L_i. L'échange L_i ↔ L_j multiplie det par -1, tandis que L_i ← L_i + c·L_j conserve det."
                },
                {
                  title: "6. Matrice Inverse A⁻¹",
                  content: "Calculée par la méthode de Gauss-Jordan sur la matrice augmentée [A | Iₙ] → [Iₙ | A⁻¹] via les 3 opérations élémentaires sur les lignes L_i. Existe si et seulement si Det(A) ≠ 0."
                },
                {
                  title: "7. Systèmes d'Équations Linéaires (AX = B)",
                  content: "Résolution par élimination de Gauss-Jordan sur [A | B]. Détecte automatiquement si la solution est unique (système de Cramer), infinie (sous-déterminé) ou impossible (incompatible)."
                }
              ].map((sec, idx) => (
                <div
                  key={idx}
                  className={`p-5 rounded-xl border ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-sm'}`}
                >
                  <h3 className="font-bold text-blue-400 mb-2">{sec.title}</h3>
                  <p className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-600'}`}>{sec.content}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* DETAILED MODAL POPUP FOR HISTORY */}
      {selectedHistoryModalItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className={`relative w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-2xl border p-6 shadow-2xl ${
            theme === 'dark' ? 'bg-slate-900 text-slate-100 border-slate-800' : 'bg-white text-slate-900 border-slate-200'
          }`}>
            {/* Modal Header */}
            <div className="flex items-start justify-between pb-4 border-b border-slate-800 mb-5">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-bold uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">
                    Détail du calcul
                  </span>
                  <span className="text-xs text-slate-400 font-mono">📅 {selectedHistoryModalItem.date || selectedHistoryModalItem.timestamp}</span>
                </div>
                <h2 className="text-2xl font-black text-blue-400">
                  {selectedHistoryModalItem.operation}
                </h2>
              </div>

              <button
                onClick={() => setSelectedHistoryModalItem(null)}
                className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-6">
              {/* 1. Informations Générales & Formule */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 font-mono text-xs">
                <div>
                  <span className="text-slate-400 block mb-1">📐 Dimensions :</span>
                  <span className="font-bold text-white text-sm">{selectedHistoryModalItem.dimensions || "N/A"}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-1">⚡ Formule / Algorithme :</span>
                  <span className="font-bold text-blue-400 text-sm">{selectedHistoryModalItem.formula || selectedHistoryModalItem.operation}</span>
                </div>
              </div>

              {/* 2. Matrices d'Entrée */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
                  <Grid className="w-4 h-4 text-blue-400" /> Matrices / Données d'Entrée
                </h3>

                <div className="flex flex-wrap items-center justify-center gap-6 p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  {(selectedHistoryModalItem.matrix_a || selectedHistoryModalItem.inputs?.A) && (
                    <MatrixDisplay
                      matrix={selectedHistoryModalItem.matrix_a || selectedHistoryModalItem.inputs?.A}
                      title={`Matrice A (${(selectedHistoryModalItem.matrix_a || selectedHistoryModalItem.inputs?.A).length}×${(selectedHistoryModalItem.matrix_a || selectedHistoryModalItem.inputs?.A)[0]?.length})`}
                      theme={theme}
                    />
                  )}

                  {(selectedHistoryModalItem.matrix_b || selectedHistoryModalItem.inputs?.B) && (
                    <>
                      <span className="text-2xl font-black text-blue-400 font-mono">
                        {selectedHistoryModalItem.operation.toLowerCase().includes('soustraction')
                          ? '−'
                          : selectedHistoryModalItem.operation.toLowerCase().includes('multiplication')
                          ? '×'
                          : selectedHistoryModalItem.operation.toLowerCase().includes('division')
                          ? '÷'
                          : '+'}
                      </span>
                      <MatrixDisplay
                        matrix={selectedHistoryModalItem.matrix_b || selectedHistoryModalItem.inputs?.B}
                        title={`Matrice B (${(selectedHistoryModalItem.matrix_b || selectedHistoryModalItem.inputs?.B).length}×${(selectedHistoryModalItem.matrix_b || selectedHistoryModalItem.inputs?.B)[0]?.length})`}
                        theme={theme}
                      />
                    </>
                  )}
                </div>
              </div>

              {/* 3. Étapes Intermédiaires et Opérations Élémentaires */}
              {selectedHistoryModalItem.steps && selectedHistoryModalItem.steps.length > 0 && (
                <div>
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
                    <BookOpen className="w-4 h-4 text-blue-400" /> Étapes Intermédiaires & Opérations Élémentaires ({selectedHistoryModalItem.steps.length})
                  </h3>

                  <div className="p-4 rounded-xl bg-slate-950 font-mono text-xs text-slate-300 border border-slate-800 max-h-96 overflow-y-auto space-y-2.5">
                    {selectedHistoryModalItem.steps.map((st: any, idx: number) => (
                      <div key={idx} className="border-b border-slate-800/80 pb-2 last:border-b-0">
                        {typeof st === 'string' ? (
                          <div className="text-slate-300 whitespace-pre-wrap">{st}</div>
                        ) : (
                          <div>
                            <span className="text-blue-400 font-bold">Étape {st.step || idx + 1} : {st.operation}</span>
                            <p className="text-slate-400 text-xs mt-0.5">{st.description}</p>
                            {st.formatted && <div className="text-emerald-400 font-mono mt-1 whitespace-pre-wrap">{st.formatted}</div>}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 4. Résultat Final & Type de Solution */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-3 flex items-center gap-1.5">
                  <CheckCircle className="w-4 h-4 text-emerald-400" /> Résultat Final du Calcul
                </h3>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col items-center justify-center">
                  {Array.isArray(selectedHistoryModalItem.result) ? (
                    <MatrixDisplay matrix={selectedHistoryModalItem.result} title="Matrice Résultat" theme={theme} />
                  ) : typeof selectedHistoryModalItem.result === 'object' && selectedHistoryModalItem.result !== null ? (
                    <div className="text-center font-mono space-y-2">
                      {selectedHistoryModalItem.result.type && (
                        <div className={`font-bold text-base ${
                          selectedHistoryModalItem.result.type === 'UNIQUE' ? 'text-emerald-400' : selectedHistoryModalItem.result.type === 'INFINITE' ? 'text-amber-400' : 'text-red-400'
                        }`}>
                          Type de Solution : {selectedHistoryModalItem.result.type === 'UNIQUE' ? 'Solution Unique' : selectedHistoryModalItem.result.type === 'INFINITE' ? 'Infinité de Solutions' : 'Aucune Solution'}
                        </div>
                      )}
                      {selectedHistoryModalItem.result.vector && (
                        <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 text-emerald-400 text-base font-bold">
                          X = [ {selectedHistoryModalItem.result.vector.join(', ')} ]
                        </div>
                      )}
                      {selectedHistoryModalItem.result.explanation && (
                        <div className="text-xs text-slate-400 mt-1 max-w-lg">
                          {selectedHistoryModalItem.result.explanation}
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="px-6 py-3 rounded-lg bg-slate-900 border border-slate-800 text-emerald-400 font-mono text-2xl font-black">
                      {String(selectedHistoryModalItem.result)}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Modal Footer Actions */}
            <div className="flex flex-wrap items-center justify-end gap-3 pt-5 border-t border-slate-800 mt-6">
              <button
                onClick={() => {
                  const itemToReload = selectedHistoryModalItem;
                  setSelectedHistoryModalItem(null);
                  reloadHistoryCalculation(itemToReload);
                }}
                className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-emerald-600/20 transition-all"
              >
                <RefreshCw className="w-4 h-4" /> Reprendre ce calcul dans l'interface
              </button>

              <button
                onClick={() => setSelectedHistoryModalItem(null)}
                className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition-colors"
              >
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}

      {/* FLOATING TOAST NOTIFICATION */}
      {toastMsg && (
        <div className="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl bg-emerald-600 text-white font-semibold text-xs shadow-2xl flex items-center gap-2 border border-emerald-400/30 animate-bounce">
          <CheckCircle className="w-4 h-4" />
          <span>{toastMsg}</span>
        </div>
      )}
    </div>
  );
}

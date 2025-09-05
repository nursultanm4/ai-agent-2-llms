import { useState, useRef, useCallback } from 'react';
import './App.css';

interface ApiResponse {
  answer: string;
  meta: Record<string, any>;
}

export default function App() {
  const [query, setQuery] = useState<string>('');
  const [answer, setAnswer] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const inputRef = useRef<HTMLInputElement>(null);
  const [controller, setController] = useState<AbortController | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);


  //  Send question to BACKEND ( UPDATED )
  const sendQuestion = async (): Promise<void> => {
    if (!query.trim()) return;

    //  просто проверяем не пустое ли сообщение отправил юзер ИЛИ на то отправил ли вообще ли он вообще сообщение - если хоть 1 из этих True, то нельзя отправить еще сообщение пока не станет False. 
    //  trim() - как strip(), убирает пробелы в начале и в конце строки.
    
    setError('');  // очиащем состояние ошибки
    setIsLoading(true);   //  уже True, т.к. функция дальше пошла 
    setAnswer('');  //  сбрасывает ответ от агента в пустую строку, нужно чтобы очистить предыдущий ответ.
    
    //   Create new AbortController for this request
    const newController = new AbortController();
    setController(newController);

    try {
      const response = await fetch('http://localhost:8000/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
        signal: newController.signal
      });

      const data: ApiResponse = await response.json();
      setAnswer(data.answer);
      
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      }
    } finally {
      setLoading(false);
      setIsLoading(false);
      setController(null);
    }
  };


  //  NEW function to handle stopping
  const handleStop = useCallback((): void => {
    if (controller) {
      controller.abort();
      setIsLoading(false);
      setController(null);
    }
  }, [controller]);


  //  Handle Enter key
  const handleKeyDown = (e: React.KeyboardEvent): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendQuestion();
    }
  };


  //  Handle magnifier click
  const handleMagnifierClick = (): void => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
    sendQuestion();
  };


  return (
    <div className="landing-bg">
      <div className="landing-content">
        <div className="landing-light" />
        <div className="landing-vignette" />
        <div className="landing-text">
          <div className="landing-greeting">Good to See You!</div>
          <h1 className="landing-title">How Can I be an Assistance?</h1>
          <div className="landing-subtitle">I’m available 24/7 for you, ask me anything.</div>
        </div>
        <div className="landing-input-row refined">
          <button className="landing-plus refined-plus" aria-label="Smile">🙂</button>
          <input
            ref={inputRef}
            className="landing-input refined-input"
            type="text"
            placeholder="Ask anything…"
            autoComplete="off"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />

          
          <button 
            onClick={isLoading ? handleStop : handleMagnifierClick}
            className="landing-icon"
            aria-label={isLoading ? "Stop generating" : "Search"}
          >
            {isLoading ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            )}
          </button>


          {isLoading && (
            <button
              onClick={handleStop}
              className="landing-stop-button"
              aria-label="Stop generating"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              </svg>
            </button>
          )}
          
        </div>
        <div style={{ minHeight: '2.5rem', marginTop: '2rem', textAlign: 'center' }}>
          {loading && <span style={{ color: '#6a7cff', fontWeight: 500 }}>Thinking…</span>}
          {error && <span style={{ color: '#ff6b6b' }}>Error: {error}</span>}
          {answer && (
            <div className="agent-output">
              {answer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
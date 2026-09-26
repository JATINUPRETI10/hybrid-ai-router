import { useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showEvaluation, setShowEvaluation] = useState(false);
  const [error, setError] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  // =====================================================
  // ANALYZE QUERY
  // =====================================================

  const analyzeQuery = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);
    setShowEvaluation(false);

    try {
      const response = await fetch(
        "https://hybrid-ai-router-gv4w.onrender.com/compare",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query,
          }),
        }
      );

      if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
          `Backend request failed: ${response.status} ${errorText}`
        );
      }

      const data = await response.json();

      console.log("COMPARE RESPONSE:", data);

      setResult(data);
    } catch (err) {
      console.error("Frontend error:", err);

      setError(
        "Unable to connect to the backend. Make sure your FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // PROVIDER
  // =====================================================

  const getProvider = () => {
    if (!result) return "—";

    if (result.selected_provider) {
      return String(result.selected_provider).toUpperCase();
    }

    if (result.route) {
      return String(result.route).toUpperCase();
    }

    if (result.provider) {
      return String(result.provider).toUpperCase();
    }

    if (result.jev) {
      return "JEV";
    }

    if (result.gemini) {
      return "GEMINI";
    }

    return "—";
  };

  // =====================================================
  // ANSWER
  // =====================================================

  const getAnswer = () => {
    if (!result) return "—";

    const provider = getProvider();

    // -------------------------
    // GEMINI
    // -------------------------

    if (provider === "GEMINI") {
      if (typeof result.answer === "string") {
        return result.answer;
      }

      if (result.answer?.text) {
        return result.answer.text;
      }

      if (result.gemini?.answer) {
        if (typeof result.gemini.answer === "string") {
          return result.gemini.answer;
        }

        if (result.gemini.answer?.text) {
          return result.gemini.answer.text;
        }
      }

      if (result.gemini?.text) {
        return result.gemini.text;
      }

      if (result.gemini?.response) {
        return result.gemini.response;
      }
    }

    // -------------------------
    // JEV
    // -------------------------

    if (result.jev?.answer?.decision) {
      return result.jev.answer.decision;
    }

    if (result.decision) {
      return result.decision;
    }

    if (result.answer?.decision) {
      return result.answer.decision;
    }

    if (typeof result.answer === "string") {
      return result.answer;
    }

    return "No answer returned.";
  };

  // =====================================================
  // CONFIDENCE
  // =====================================================

  const getConfidence = () => {
    if (!result) return null;

    let confidence = result.jev?.answer?.confidence;

    if (
      confidence === undefined ||
      confidence === null
    ) {
      confidence = result.confidence;
    }

    if (
      confidence === undefined ||
      confidence === null
    ) {
      return null;
    }

    confidence = Number(confidence);

    if (Number.isNaN(confidence)) {
      return null;
    }

    if (confidence <= 1) {
      return Math.round(confidence * 100);
    }

    return Math.round(confidence);
  };

  // =====================================================
  // FORMATTERS
  // =====================================================

  const formatLatency = (value) => {
    if (
      value === undefined ||
      value === null
    ) {
      return "—";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return "—";
    }

    return `${(number / 1000).toFixed(2)}s`;
  };

  const formatNumber = (value) => {
    if (
      value === undefined ||
      value === null
    ) {
      return "—";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return String(value);
    }

    return number.toLocaleString();
  };

  const formatCost = (value) => {
    if (
      value === undefined ||
      value === null
    ) {
      return "$0.000000";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return "$0.000000";
    }

    return `$${number.toFixed(6)}`;
  };

  const getInputTokens = (provider) => {
    if (!provider) return null;

    return (
      provider.input_tokens ??
      provider.inputTokens ??
      provider.usage?.input_tokens ??
      provider.usage?.inputTokens ??
      provider.usage?.prompt_tokens ??
      null
    );
  };

  const getOutputTokens = (provider) => {
    if (!provider) return null;

    return (
      provider.output_tokens ??
      provider.outputTokens ??
      provider.usage?.output_tokens ??
      provider.usage?.outputTokens ??
      provider.usage?.completion_tokens ??
      null
    );
  };

  const getTotalTokens = (provider) => {
    if (!provider) return null;

    if (
      provider.total_tokens !== undefined &&
      provider.total_tokens !== null
    ) {
      return provider.total_tokens;
    }

    const input = getInputTokens(provider);
    const output = getOutputTokens(provider);

    if (
      input === null &&
      output === null
    ) {
      return null;
    }

    return (
      Number(input || 0) +
      Number(output || 0)
    );
  };

  const getLatency = (provider) => {
    if (!provider) return null;

    return (
      provider.latency_ms ??
      provider.latencyMs ??
      provider.server_latency_ms ??
      provider.serverLatencyMs ??
      null
    );
  };

  const getCost = (provider) => {
    if (!provider) return null;

    return provider.cost ?? null;
  };

  // =====================================================
  // DATA
  // =====================================================

  const jev = result?.jev;
  const gemini = result?.gemini;
  const comparison = result?.comparison;
  const confidence = getConfidence();

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className={`app ${darkMode ? "dark" : ""}`}>

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="header">

        <div className="brand">
          <h1>Hybrid AI Router</h1>

          <p>
            JEV + Gemini · Intelligent AI routing
          </p>
        </div>

        <div className="header-actions">

          <div className="status">
            <span className="dot"></span>
            System Online
          </div>

          <button
            className="theme-toggle"
            onClick={() =>
              setDarkMode(!darkMode)
            }
            type="button"
          >
            {darkMode ? "☀ Light" : "☾ Dark"}
          </button>

        </div>

      </header>


      {/* =================================================
          MAIN
      ================================================= */}

      <main>

        {/* HERO */}

        <section className="hero">

          <div className="badge">
            AI ROUTING ENGINE
          </div>

          <h2>
            Ask anything.
            <br />

            <span>
              We route it intelligently.
            </span>
          </h2>

          <p className="subtitle">
            A hybrid AI system that automatically
            chooses between JEV and Gemini based
            on the nature of your query.
          </p>

        </section>


        {/* =================================================
            QUERY CARD
        ================================================= */}

        <section className="query-card">

          <div className="card-header">

            <div>

              <h3>
                YOUR QUERY
              </h3>

              <p>
                Ask a question or describe a task
              </p>

            </div>

            <span className="text-only">
              TEXT
            </span>

          </div>


          <textarea
            value={query}
            onChange={(e) =>
              setQuery(e.target.value)
            }
            placeholder="e.g. Is this transaction high-risk?"
          />


          <div className="query-footer">

            <span>
              {query.length} characters
            </span>

            <button
              onClick={analyzeQuery}
              disabled={
                !query.trim() || loading
              }
              type="button"
            >
              {loading
                ? "Analyzing..."
                : "Analyze →"}
            </button>

          </div>

        </section>


        {/* =================================================
            ERROR
        ================================================= */}

        {error && (
          <div className="error-box">

            <span>⚠</span>

            {error}

          </div>
        )}


        {/* =================================================
            RESPONSE
        ================================================= */}

        {result && (

          <section className="response-section">

            <div className="response-label">
              RESPONSE
            </div>


            {/* =================================================
                ANSWER CARD
            ================================================= */}

            <div className="answer-card">

              <div className="answer-header">

                <div className="provider-name">

                  <span className="provider-dot"></span>

                  {getProvider()}

                </div>

                <span className="routed">
                  ROUTED
                </span>

              </div>


              {/* =================================================
                  ACTUAL ANSWER
              ================================================= */}

              <div className="answer-content">

                <div className="answer-markdown">

                  <ReactMarkdown>
                    {String(getAnswer())}
                  </ReactMarkdown>

                </div>


                {confidence !== null && (

                  <div className="confidence">

                    Confidence

                    <strong>
                      {confidence}%
                    </strong>

                  </div>

                )}

              </div>

            </div>


            {/* =================================================
                EVALUATION BUTTON
            ================================================= */}

            <button
              className={`evaluation-button ${
                showEvaluation ? "open" : ""
              }`}
              onClick={() =>
                setShowEvaluation(
                  !showEvaluation
                )
              }
              type="button"
            >

              <div className="evaluation-left">

                <div className="evaluation-icon">
                  ✦
                </div>

                <div>

                  <strong>
                    View Evaluation & Comparison
                  </strong>

                  <span>
                    Routing performance,
                    latency, tokens & cost
                  </span>

                </div>

              </div>


              <span className="arrow">
                {showEvaluation
                  ? "↑"
                  : "↓"}
              </span>

            </button>


            {/* =================================================
                EVALUATION
            ================================================= */}

            {showEvaluation && (

              <div className="evaluation-panel">


                {/* =================================================
                    ROUTING DECISION
                ================================================= */}

                <div className="eval-block">

                  <div className="eval-title">

                    <span>
                      01
                    </span>

                    <div>

                      <h3>
                        Routing Decision
                      </h3>

                      <p>
                        The routing model selected
                        the appropriate backend.
                      </p>

                    </div>

                  </div>


                  <div className="route-result">

                    <div>

                      <span className="eval-label">
                        SELECTED PROVIDER
                      </span>

                      <strong>
                        {getProvider()}
                      </strong>

                    </div>


                    <div>

                      <span className="eval-label">
                        DECISION
                      </span>

                      <strong>
                        {getProvider() === "JEV"
                          ? (
                              result.jev?.answer?.decision ??
                              result.decision ??
                              "—"
                            )
                          : "Generated response"}
                      </strong>

                    </div>

                  </div>


                  {confidence !== null && (

                    <div className="confidence-eval">

                      <span className="eval-label">
                        CONFIDENCE
                      </span>

                      <strong>
                        {confidence}%
                      </strong>

                    </div>

                  )}

                </div>


                {/* =================================================
                    PERFORMANCE
                ================================================= */}

                <div className="eval-block">

                  <div className="eval-title">

                    <span>
                      02
                    </span>

                    <div>

                      <h3>
                        Performance Comparison
                      </h3>

                      <p>
                        Executed provider vs
                        alternative provider.
                      </p>

                    </div>

                  </div>


                  <div className="comparison-grid">


                    {/* JEV */}

                    <div className="provider-card">

                      <div className="provider-heading">

                        <div>

                          <span className="small-label">
                            EXECUTED
                          </span>

                          <h3>
                            ⚡ JEV
                          </h3>

                        </div>

                        <span className="used">
                          USED
                        </span>

                      </div>


                      <div className="metrics">

                        <div>
                          <span>
                            Latency
                          </span>

                          <strong>
                            {formatLatency(
                              getLatency(jev)
                            )}
                          </strong>
                        </div>


                        <div>
                          <span>
                            Input Tokens
                          </span>

                          <strong>
                            {formatNumber(
                              getInputTokens(jev)
                            )}
                          </strong>
                        </div>


                        <div>
                          <span>
                            Output Tokens
                          </span>

                          <strong>
                            {formatNumber(
                              getOutputTokens(jev)
                            )}
                          </strong>
                        </div>


                        <div>
                          <span>
                            Total Tokens
                          </span>

                          <strong>
                            {formatNumber(
                              getTotalTokens(jev)
                            )}
                          </strong>
                        </div>


                        <div>
                          <span>
                            Cost
                          </span>

                          <strong>
                            {formatCost(
                              getCost(jev)
                            )}
                          </strong>
                        </div>

                      </div>

                    </div>


                    {/* GEMINI */}

                    <div className="provider-card">

                      <div className="provider-heading">

                        <div>

                          <span className="small-label">
                            ALTERNATIVE
                          </span>

                          <h3>
                            ✦ Gemini
                          </h3>

                        </div>

                      </div>


                      <div className="metrics">

                        <div>
                          <span>
                            Latency
                          </span>

                          <strong>
                            {formatLatency(
                              getLatency(gemini)
                            )}
                          </strong>
                        </div>


                        <div>
                          <span>
                            Input Tokens
                          </span>

                          <strong>
                            {formatNumber(
                              getInputTokens(gemini)
                            )}
                          </strong>
                        </div>


                        <div>
                          <span>
                            Output Tokens
                          </span>

                          <strong>
                            {formatNumber(
                              getOutputTokens(gemini)
                            )}
                          </strong>
                        </div>


                        <div>
                          <span>
                            Total Tokens
                          </span>

                          <strong>
                            {formatNumber(
                              getTotalTokens(gemini)
                            )}
                          </strong>
                        </div>


                        <div>
                          <span>
                            Cost
                          </span>

                          <strong>
                            {formatCost(
                              getCost(gemini)
                            )}
                          </strong>
                        </div>

                      </div>

                    </div>

                  </div>

                </div>


                {/* =================================================
                    SUMMARY
                ================================================= */}

                <div className="evaluation-summary">

                  <div>

                    <span>
                      TIME DIFFERENCE
                    </span>

                    <strong>
                      {comparison?.time_difference_ms !==
                        undefined &&
                      comparison?.time_difference_ms !==
                        null
                        ? `${(
                            Number(
                              comparison.time_difference_ms
                            ) / 1000
                          ).toFixed(2)}s`
                        : "—"}
                    </strong>

                  </div>


                  <div>

                    <span>
                      LATENCY IMPROVEMENT
                    </span>

                    <strong>
                      {comparison?.time_saved_percent !==
                        undefined &&
                      comparison?.time_saved_percent !==
                        null
                        ? `${comparison.time_saved_percent}%`
                        : "—"}
                    </strong>

                  </div>


                  <div>

                    <span>
                      FASTER PROVIDER
                    </span>

                    <strong>
                      {comparison?.faster_provider
                        ? String(
                            comparison.faster_provider
                          ).toUpperCase()
                        : "—"}
                    </strong>

                  </div>

                </div>

              </div>

            )}

          </section>

        )}

      </main>


      {/* =================================================
          FOOTER
      ================================================= */}

      <footer>

        Hybrid AI Router
        &nbsp;·&nbsp;
        JEV + Gemini
        &nbsp;·&nbsp;
        Performance-aware AI routing

      </footer>

    </div>
  );
}

export default App;
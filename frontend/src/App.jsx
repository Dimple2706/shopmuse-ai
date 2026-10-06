import { useState } from "react";
import {
  Sparkles,
  ShoppingBag,
  Heart,
  WandSparkles
} from "lucide-react";

import ChatBox from "./components/ChatBox";
import ProductCard from "./components/ProductCard";
import AgentActivity from "./components/AgentActivity";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) {
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            session_id: "demo-session",
            message: message
          })
        }
      );

      const data = await res.json();

      setResponse(data);
      setMessage("");

    } catch (error) {
      console.error(error);

      setResponse({
        type: "error",
        message:
          "Oops! I couldn't connect to ShopMuse. Please make sure the backend is running."
      });

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* =========================
          NAVBAR
      ========================= */}

      <nav className="navbar">

        <div className="logo">

          <div className="logo-icon">
            <Sparkles size={18} />
          </div>

          <span>ShopMuse</span>

          <small>AI</small>

        </div>

        <div className="nav-links">

          <span>Discover</span>

          <span>How it works</span>

          <button className="favorites">
            <Heart size={17} />
            Favorites
          </button>

        </div>

      </nav>


      {/* =========================
          HERO SECTION
      ========================= */}

      <section className="hero">

        <div className="hero-badge">

          <Sparkles size={15} />

          Your personal shopping muse

        </div>

        <h1>
          Shopping,
          <br />
          <span>but make it magical.</span>
        </h1>

        <p>
          Tell ShopMuse what you're looking for.
          <br />
          We'll understand the details and find
          your perfect match.
        </p>

      </section>


      {/* =========================
          MAIN CONTENT
      ========================= */}

      <main className="main-content">

        <div className="chat-section">

          {/* CHAT BOX */}

          <ChatBox
            message={message}
            setMessage={setMessage}
            onSend={sendMessage}
            loading={loading}
          />


          {/* QUICK PROMPTS */}

          <div className="quick-prompts">

            <span>Try asking:</span>

            <button
              onClick={() =>
                setMessage(
                  "I need a gift for my dad who loves hiking and has bad knees, budget 100"
                )
              }
            >
              🎁 Gift for dad
            </button>

            <button
              onClick={() =>
                setMessage(
                  "I need something lightweight for hiking under 80"
                )
              }
            >
              🥾 Hiking essentials
            </button>

            <button
              onClick={() =>
                setMessage(
                  "I need something for yoga under 60"
                )
              }
            >
              🧘 Yoga
            </button>

          </div>


          {/* =========================
              AGENT ACTIVITY
          ========================= */}

          {loading && <AgentActivity />}


          {/* =========================
              CLARIFICATION
          ========================= */}

          {response?.type === "clarification" && (

            <div className="clarification-card">

              <WandSparkles size={22} />

              <div>

                <strong>
                  Let's narrow it down ✨
                </strong>

                <p>
                  {response.question}
                </p>

              </div>

            </div>

          )}


          {/* =========================
              FALLBACK / ALTERNATIVES
          ========================= */}

          {response?.type === "fallback" && (

            <section className="results">

              <div className="fallback-card">

                <Sparkles size={22} />

                <div>

                  <strong>
                    Let's try something close ✨
                  </strong>

                  <p>
                    {response.message}
                  </p>

                </div>

              </div>


              {/* ALTERNATIVE PRODUCTS */}

              {response.products &&
                response.products.length > 0 && (

                  <>

                    <div className="results-header">

                      <div>

                        <span className="eyebrow">
                          CLOSE ALTERNATIVES
                        </span>

                        <h2>
                          Worth considering
                        </h2>

                      </div>

                      <ShoppingBag size={24} />

                    </div>


                    <div className="product-grid">

                      {response.products.map(
                        (product, index) => (

                          <ProductCard
                            key={index}
                            item={{
                              product: product,

                              fit_score: 0,

                              reasons: [
                                "Closest available option"
                              ],

                              explanation:
                                "A nearby alternative based on your shopping requirements."
                            }}
                          />

                        )
                      )}

                    </div>

                  </>

                )}

            </section>

          )}


          {/* =========================
              NORMAL RECOMMENDATIONS
          ========================= */}

          {response?.type === "recommendation" && (

            <section className="results">

              <div className="results-header">

                <div>

                  <span className="eyebrow">
                    CURATED FOR YOU
                  </span>

                  <h2>
                    Your perfect picks
                  </h2>

                </div>

                <ShoppingBag size={24} />

              </div>


              <div className="product-grid">

                {response.products.map(
                  (item, index) => (

                    <ProductCard
                      item={item}
                      key={index}
                    />

                  )
                )}

              </div>

            </section>

          )}


          {/* =========================
              ERROR
          ========================= */}

          {response?.type === "error" && (

            <div className="error-card">

              <p>
                {response.message}
              </p>

            </div>

          )}

        </div>

      </main>


      {/* =========================
          FOOTER
      ========================= */}

      <footer>

        <span>
          Made with ♡ by ShopMuse AI
        </span>

        <span>
          Intelligent shopping, simplified.
        </span>

      </footer>

    </div>
  );
}

export default App;



import { useState } from "react";

import {
  Sparkles,
  ShoppingBag,
  Heart,
  WandSparkles,
  SlidersHorizontal,
  Check,
  RotateCcw,
  GitCompare,
  X,
  Crown
} from "lucide-react";

import ChatBox from "./components/ChatBox";
import ProductCard from "./components/ProductCard";
import AgentActivity from "./components/AgentActivity";


function App() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  // Compare mode
  const [compareItems, setCompareItems] = useState([]);
  const [showComparison, setShowComparison] = useState(false);


  // =====================================================
  // SEND MESSAGE
  // =====================================================

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


  // =====================================================
  // REFINEMENT
  // =====================================================

  const sendRefinement = (text) => {

    setMessage(text);

    setTimeout(() => {

      document
        .querySelector(".chat-box input")
        ?.focus();

    }, 50);

  };


  // =====================================================
  // COMPARE
  // =====================================================

  const toggleCompare = (item) => {

    setCompareItems((current) => {

      const exists = current.some(
        (selected) =>
          selected.product.id ===
          item.product.id
      );


      // Remove if already selected

      if (exists) {

        return current.filter(
          (selected) =>
            selected.product.id !==
            item.product.id
        );

      }


      // Maximum 3 products

      if (current.length >= 3) {

        return current;

      }


      // Add product

      return [
        ...current,
        item
      ];

    });

  };


  // =====================================================
  // BEST COMPARED PRODUCT
  // =====================================================

  const bestComparedProduct =
    compareItems.length > 0
      ? compareItems.reduce(
          (best, current) =>
            current.fit_score >
            best.fit_score
              ? current
              : best
        )
      : null;


  // =====================================================
  // INTENT CHIPS
  // =====================================================

  const renderPreferenceChips = () => {

    if (
      response?.type !== "recommendation" ||
      !response.intent
    ) {

      return null;

    }


    const {
      category,
      budget,
      preferences = []
    } = response.intent;


    return (

      <div className="intent-summary">

        <div className="intent-summary-top">

          <div>

            <span className="eyebrow">
              SHOPMUSE UNDERSTOOD
            </span>

            <h3>
              Your shopping mood ✨
            </h3>

          </div>


          <div className="intent-confidence">

            <Check size={13} />

            {Math.round(
              (response.intent.confidence || 0) *
              100
            )}% understood

          </div>

        </div>


        <div className="intent-chips">

          {category && (

            <span className="intent-chip primary">

              ✦ {category}

            </span>

          )}


          {budget && (

            <span className="intent-chip">

              ♡ Under ${budget}

            </span>

          )}


          {preferences.map(
            (preference, index) => (

              <span
                className="intent-chip"
                key={index}
              >

                <Check size={12} />

                {preference}

              </span>

            )
          )}

        </div>

      </div>

    );

  };


  // =====================================================
  // REPLANNING NOTICE
  // =====================================================

  const renderReplanningNotice = () => {

    if (
      response?.type !== "recommendation" ||
      !response.plan?.includes("replanning")
    ) {

      return null;

    }


    return (

      <div className="tradeoff-card">

        <div className="tradeoff-icon">

          <RotateCcw size={18} />

        </div>


        <div className="tradeoff-content">

          <strong>
            I made a tiny trade-off for you ✨
          </strong>

          <p>

            I couldn't find products matching every
            preference within your budget, so I relaxed
            the least achievable requirement and found
            the closest matches instead.

          </p>

        </div>


        <span className="tradeoff-badge">

          SMART PIVOT

        </span>

      </div>

    );

  };


  // =====================================================
  // COMPARISON MODAL
  // =====================================================

  const renderComparisonModal = () => {

    if (!showComparison) {

      return null;

    }


    return (

      <div
        className="modal-overlay"
        onClick={() =>
          setShowComparison(false)
        }
      >

        <div
          className="comparison-modal"
          onClick={(e) =>
            e.stopPropagation()
          }
        >

          {/* CLOSE */}

          <button
            className="comparison-close"
            onClick={() =>
              setShowComparison(false)
            }
          >

            <X size={20} />

          </button>


          {/* HEADER */}

          <div className="comparison-heading">

            <span className="eyebrow">

              SHOPMUSE COMPARISON

            </span>


            <h2>

              Let's compare your picks ✨

            </h2>


            <p>

              Here's how your selected products
              stack up.

            </p>

          </div>


          {/* PRODUCTS */}

          <div className="comparison-grid">

            {compareItems.map(
              (item) => {

                const isBest =
                  bestComparedProduct?.product.id ===
                  item.product.id;


                return (

                  <div
                    className={`comparison-product ${
                      isBest
                        ? "comparison-best"
                        : ""
                    }`}
                    key={item.product.id}
                  >

                    {/* BEST BADGE */}

                    {isBest && (

                      <div className="best-badge">

                        <Crown size={12} />

                        BEST MATCH

                      </div>

                    )}


                    {/* IMAGE */}

                    <div className="comparison-image">

                      <Sparkles size={30} />

                    </div>


                    {/* NAME */}

                    <h3>

                      {item.product.name}

                    </h3>


                    {/* SCORE */}

                    <div className="comparison-score">

                      ✨ {item.fit_score}%

                    </div>


                    {/* PRICE */}

                    <div className="comparison-row">

                      <span>
                        Price
                      </span>

                      <strong>
                        ${item.product.price}
                      </strong>

                    </div>


                    {/* RATING */}

                    <div className="comparison-row">

                      <span>
                        Rating
                      </span>

                      <strong>

                        ⭐ {item.product.rating}

                      </strong>

                    </div>


                    {/* CATEGORY */}

                    <div className="comparison-row">

                      <span>
                        Category
                      </span>

                      <strong>

                        {item.product.category}

                      </strong>

                    </div>


                    {/* REASONS */}

                    <div className="comparison-row">

                      <span>
                        Match
                      </span>

                      <strong>

                        {item.reasons.length}
                        {" "}
                        matching reasons

                      </strong>

                    </div>


                    {/* TAGS */}

                    <div className="comparison-tags">

                      {item.product.tags.map(
                        (tag, index) => (

                          <span key={index}>

                            {tag}

                          </span>

                        )
                      )}

                    </div>


                    {/* REMOVE */}

                    <button
                      className="remove-comparison"
                      onClick={() =>
                        toggleCompare(item)
                      }
                    >

                      Remove

                    </button>

                  </div>

                );

              }
            )}

          </div>


          {/* VERDICT */}

          {bestComparedProduct && (

            <div className="comparison-verdict">

              <Sparkles size={18} />

              <div>

                <strong>

                  ShopMuse's recommendation

                </strong>


                <p>

                  I'd choose{" "}

                  <b>
                    {
                      bestComparedProduct.product.name
                    }
                  </b>

                  {" "}
                  because it has the strongest
                  overall fit for your request.

                </p>

              </div>

            </div>

          )}

        </div>

      </div>

    );

  };


  // =====================================================
  // MAIN UI
  // =====================================================

  return (

    <div className="app">


      {/* =================================================
          NAVBAR
          ================================================= */}

      <nav className="navbar">

        <div className="logo">

          <div className="logo-icon">

            <Sparkles size={18} />

          </div>


          <span>
            ShopMuse
          </span>


          <small>
            AI
          </small>

        </div>


        <div className="nav-links">

          <span>
            Discover
          </span>


          <span>
            How it works
          </span>


          <button className="favorites">

            <Heart size={17} />

            Favorites

          </button>

        </div>

      </nav>



      {/* =================================================
          HERO
          ================================================= */}

      <section className="hero">

        <div className="hero-badge">

          <Sparkles size={15} />

          Your personal shopping muse

        </div>


        <h1>

          Shopping,

          <br />

          <span>
            but make it magical.
          </span>

        </h1>


        <p>

          Tell ShopMuse what you're looking for.

          <br />

          We'll understand the details and find
          your perfect match.

        </p>

      </section>



      {/* =================================================
          MAIN
          ================================================= */}

      <main className="main-content">

        <div className="chat-section">


          {/* CHAT */}

          <ChatBox
            message={message}
            setMessage={setMessage}
            onSend={sendMessage}
            loading={loading}
          />



          {/* QUICK PROMPTS */}

          <div className="quick-prompts">

            <span>
              Try asking:
            </span>


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



          {/* AGENT ACTIVITY */}

          {loading && (

            <AgentActivity />

          )}



          {/* =================================================
              CLARIFICATION
              ================================================= */}

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



          {/* =================================================
              FALLBACK
              ================================================= */}

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
                              product,
                              fit_score: 0,
                              reasons: [
                                "Closest available option"
                              ],
                              explanation:
                                "A nearby alternative based on your shopping requirements."
                            }}

                            isSelected={
                              compareItems.some(
                                (selected) =>
                                  selected.product.id ===
                                  product.id
                              )
                            }

                            onCompare={
                              toggleCompare
                            }

                          />

                        )
                      )}

                    </div>


                    {/* FALLBACK COMPARE BAR */}

                    {compareItems.length > 0 && (

                      <div className="compare-floating-bar">

                        <div className="compare-info">

                          <div className="compare-icon">

                            <GitCompare size={17} />

                          </div>


                          <div>

                            <strong>

                              Compare your picks

                            </strong>


                            <span>

                              {compareItems.length}
                              {" "}
                              of 3 selected

                            </span>

                          </div>

                        </div>


                        <div className="compare-actions">

                          <button
                            className="clear-compare"
                            onClick={() =>
                              setCompareItems([])
                            }
                          >

                            Clear

                          </button>


                          <button
                            className="compare-main-button"
                            disabled={
                              compareItems.length < 2
                            }
                            onClick={() =>
                              setShowComparison(true)
                            }
                          >

                            <GitCompare size={15} />

                            Compare

                          </button>

                        </div>

                      </div>

                    )}

                  </>

                )}

            </section>

          )}



          {/* =================================================
              RECOMMENDATIONS
              ================================================= */}

          {response?.type === "recommendation" && (

            <section className="results">


              {/* RESULTS HEADER */}

              <div className="results-header">

                <div>

                  <span className="eyebrow">

                    CURATED FOR YOU

                  </span>


                  <h2>

                    Your perfect picks

                  </h2>


                  <p className="result-count">

                    {response.products?.length || 0}

                    {" "}

                    handpicked matches for your request

                  </p>

                </div>


                <div className="results-header-icon">

                  <ShoppingBag size={24} />

                </div>

              </div>



              {/* INTENT */}

              {renderPreferenceChips()}



              {/* REPLANNING */}

              {renderReplanningNotice()}



              {/* REFINEMENT */}

              <div className="refinement-bar">

                <div className="refinement-title">

                  <SlidersHorizontal size={15} />

                  <span>

                    Refine your picks

                  </span>

                </div>


                <div className="refinement-options">

                  <button
                    onClick={() =>
                      sendRefinement(
                        "make it cheaper"
                      )
                    }
                  >

                    ♡ Cheaper

                  </button>


                  <button
                    onClick={() =>
                      sendRefinement(
                        "make it more comfortable"
                      )
                    }
                  >

                    ☁ More comfortable

                  </button>


                  <button
                    onClick={() =>
                      sendRefinement(
                        "show me more premium options"
                      )
                    }
                  >

                    ✦ More premium

                  </button>


                  <button
                    onClick={() =>
                      sendRefinement(
                        "show me lightweight options"
                      )
                    }
                  >

                    ♧ Lightweight

                  </button>


                  <button
                    onClick={() =>
                      sendRefinement(
                        "show me different alternatives"
                      )
                    }
                  >

                    ↻ Alternatives

                  </button>

                </div>

              </div>



              {/* PRODUCT GRID */}

              <div className="product-grid">

                {response.products.map(
                  (item, index) => (

                    <ProductCard
                      item={item}

                      key={item.product.id || index}

                      isTopPick={
                        index === 0
                      }

                      isSelected={
                        compareItems.some(
                          (selected) =>
                            selected.product.id ===
                            item.product.id
                        )
                      }

                      onCompare={
                        toggleCompare
                      }

                    />

                  )
                )}

              </div>



              {/* =================================================
                  COMPARE FLOATING BAR
                  ================================================= */}

              {compareItems.length > 0 && (

                <div className="compare-floating-bar">

                  <div className="compare-info">

                    <div className="compare-icon">

                      <GitCompare size={17} />

                    </div>


                    <div>

                      <strong>

                        Compare your picks

                      </strong>


                      <span>

                        {compareItems.length}
                        {" "}
                        of 3 selected

                      </span>

                    </div>

                  </div>


                  <div className="compare-actions">


                    <button
                      className="clear-compare"
                      onClick={() =>
                        setCompareItems([])
                      }
                    >

                      Clear

                    </button>


                    <button
                      className="compare-main-button"
                      disabled={
                        compareItems.length < 2
                      }
                      onClick={() =>
                        setShowComparison(true)
                      }
                    >

                      <GitCompare size={15} />

                      Compare

                    </button>

                  </div>

                </div>

              )}

            </section>

          )}



          {/* =================================================
              ERROR
              ================================================= */}

          {response?.type === "error" && (

            <div className="error-card">

              <p>

                {response.message}

              </p>

            </div>

          )}

        </div>

      </main>



      {/* =================================================
          FOOTER
          ================================================= */}

      <footer>

        <span>

          Made with ♡ by ShopMuse AI

        </span>


        <span>

          Intelligent shopping, simplified.

        </span>

      </footer>



      {/* =================================================
          COMPARISON MODAL
          ================================================= */}

      {renderComparisonModal()}

    </div>

  );

}


export default App;


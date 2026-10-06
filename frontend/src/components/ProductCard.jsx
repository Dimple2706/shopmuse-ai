import {
  Heart,
  Star,
  Sparkles,
  ExternalLink,
  ChevronDown,
  X,
  ShoppingBag
} from "lucide-react";

import { useState } from "react";

function ProductCard({ item }) {

  const [showWhy, setShowWhy] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  const product = item.product;

  return (
    <>
      <div className="product-card">

        <div className="product-image">
          <Sparkles size={28} />
        </div>

        <div className="product-info">

          <div className="product-top">

            <span className="product-category">
              {product.category}
            </span>

            <button className="heart-button">
              <Heart size={18} />
            </button>

          </div>

          <h3>
            {product.name}
          </h3>

          <div className="rating">

            <Star
              size={15}
              fill="currentColor"
            />

            {product.rating}

          </div>

          <p className="price">
            ${product.price}
          </p>

          <div className="match-score">
            ✨ {item.fit_score}% Match
          </div>

          <p className="explanation">
            {item.explanation}
          </p>

          <div className="reasons">

            {item.reasons.map(
              (reason, index) => (
                <span key={index}>
                  ✓ {reason}
                </span>
              )
            )}

          </div>

          <button
            className="why-button"
            onClick={() =>
              setShowWhy(!showWhy)
            }
          >

            <Sparkles size={15} />

            Why this product?

            <ChevronDown
              size={15}
              style={{
                transform: showWhy
                  ? "rotate(180deg)"
                  : "rotate(0deg)",
                transition: "0.2s"
              }}
            />

          </button>

          {showWhy && (

            <div className="why-box">

              <strong>
                Why ShopMuse picked this ✨
              </strong>

              <p>
                This product scored highly because it{" "}
                {item.reasons.length > 0
                  ? item.reasons.join(", ") + "."
                  : "closely matches your requirements."
                }
              </p>

            </div>

          )}

          <button
            className="view-button"
            onClick={() =>
              setShowDetails(true)
            }
          >

            View Product

            <ExternalLink size={14} />

          </button>

        </div>

      </div>

      {showDetails && (

        <div
          className="modal-overlay"
          onClick={() =>
            setShowDetails(false)
          }
        >

          <div
            className="product-modal"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <button
              className="modal-close"
              onClick={() =>
                setShowDetails(false)
              }
            >
              <X size={20} />
            </button>

            <div className="modal-image">
              <Sparkles size={45} />
            </div>

            <span className="product-category">
              {product.category}
            </span>

            <h2>
              {product.name}
            </h2>

            <div className="modal-rating">

              <Star
                size={17}
                fill="currentColor"
              />

              {product.rating}

            </div>

            <p className="modal-price">
              ${product.price}
            </p>

            <div className="modal-match">
              ✨ {item.fit_score}% ShopMuse Match
            </div>

            <p className="modal-description">
              {item.explanation}
            </p>

            <div className="modal-tags">

              {product.tags.map(
                (tag, index) => (
                  <span key={index}>
                    {tag}
                  </span>
                )
              )}

            </div>

            <button
              className="modal-shop-button"
              onClick={() =>
                alert(
                  "Shopping integration can be connected here."
                )
              }
            >

              <ShoppingBag size={17} />

              Shop this product

            </button>

          </div>

        </div>

      )}

    </>
  );
}

export default ProductCard;
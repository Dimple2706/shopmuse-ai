import {
  Heart,
  Star,
  Sparkles,
  ExternalLink,
  ChevronDown,
  X,
  ShoppingBag,
  GitCompare,
  Crown
} from "lucide-react";

import { useState } from "react";


function ProductCard({
  item,
  isTopPick = false,
  isSelected = false,
  onCompare
}) {

  const [showWhy, setShowWhy] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [liked, setLiked] = useState(false);

  const product = item.product;


  return (
    <>
      <div
        className={`product-card ${
          isTopPick
            ? "top-pick-card"
            : ""
        }`}
      >

        {/* SHOPMUSE PICK */}

        {isTopPick && (

          <div className="shopmuse-pick">

            <Crown size={13} />

            SHOPMUSE PICK

          </div>

        )}


        {/* PRODUCT IMAGE */}

        <div className="product-image">

          <Sparkles size={28} />

          {isTopPick && (

            <div className="pick-glow">
              ✦
            </div>

          )}

        </div>


        <div className="product-info">


          {/* TOP ROW */}

          <div className="product-top">

            <span className="product-category">
              {product.category}
            </span>


            <button
              className={`heart-button ${
                liked
                  ? "liked"
                  : ""
              }`}
              onClick={() =>
                setLiked(!liked)
              }
            >

              <Heart
                size={18}
                fill={
                  liked
                    ? "currentColor"
                    : "none"
                }
              />

            </button>

          </div>


          {/* NAME */}

          <h3>
            {product.name}
          </h3>


          {/* RATING */}

          <div className="rating">

            <Star
              size={15}
              fill="currentColor"
            />

            {product.rating}

          </div>


          {/* PRICE */}

          <p className="price">
            ${product.price}
          </p>


          {/* MATCH */}

          <div className="match-score">

            ✨ {item.fit_score}% Match

          </div>


          {/* EXPLANATION */}

          <p className="explanation">
            {item.explanation}
          </p>


          {/* REASONS */}

          <div className="reasons">

            {item.reasons.map(
              (reason, index) => (

                <span key={index}>

                  ✓ {reason}

                </span>

              )
            )}

          </div>


          {/* WHY BUTTON */}

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
                transform:
                  showWhy
                    ? "rotate(180deg)"
                    : "rotate(0deg)",

                transition:
                  "0.2s"
              }}
            />

          </button>


          {/* WHY BOX */}

          {showWhy && (

            <div className="why-box">

              <strong>
                Why ShopMuse picked this ✨
              </strong>

              <p>

                This product scored highly
                because it{" "}

                {item.reasons.length > 0
                  ? item.reasons.join(
                      ", "
                    ) + "."
                  : "closely matches your requirements."
                }

              </p>

            </div>

          )}


          {/* ACTION ROW */}

          <div className="product-actions">


            {/* COMPARE */}

            <button
              className={`compare-button ${
                isSelected
                  ? "selected"
                  : ""
              }`}
              onClick={() =>
                onCompare?.(item)
              }
            >

              {isSelected ? (
                <CheckIcon />
              ) : (
                <GitCompare size={14} />
              )}

              {isSelected
                ? "Added"
                : "Compare"}

            </button>


            {/* VIEW */}

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

      </div>


      {/* PRODUCT MODAL */}

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

              ✨ {item.fit_score}%
              {" "}
              ShopMuse Match

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


/* Small reusable check icon */

function CheckIcon() {

  return (
    <span className="compare-check">
      ✓
    </span>
  );

}


export default ProductCard;
import {
  Sparkles,
  Search,
  Brain,
  SlidersHorizontal,
  CheckCircle,
  MessageCircle,
  ShieldCheck
} from "lucide-react";

function AgentActivity({ plan = [] }) {

  const agentMap = {
    intent_extraction: {
      icon: Brain,
      name: "Intent Analysis",
      status: "Understanding your request"
    },

    catalog_mapping: {
      icon: SlidersHorizontal,
      name: "Preference Mapping",
      status: "Mapping your preferences"
    },

    candidate_retrieval: {
      icon: Search,
      name: "Product Search",
      status: "Searching the catalog"
    },

    product_ranking: {
      icon: Sparkles,
      name: "Fit Ranking",
      status: "Finding your best matches"
    },

    explanation: {
      icon: MessageCircle,
      name: "Explanation Agent",
      status: "Preparing personalized explanations"
    },

    reviewer: {
      icon: ShieldCheck,
      name: "Quality Review",
      status: "Checking recommendations"
    }
  };

  const visibleAgents =
    plan.length > 0
      ? plan
          .map((step) => agentMap[step])
          .filter(Boolean)
      : Object.values(agentMap);

  return (
    <div className="agent-panel">

      <div className="agent-header">
        <Sparkles size={18} />
        <span>ShopMuse Intelligence</span>
      </div>

      {visibleAgents.map((agent, index) => {

        const Icon = agent.icon;

        return (
          <div
            className="agent-item"
            key={index}
          >

            <div className="agent-icon">
              <Icon size={16} />
            </div>

            <div>
              <strong>
                {agent.name}
              </strong>

              <p>
                {agent.status}
              </p>
            </div>

            <CheckCircle
              size={16}
              className="agent-check"
            />

          </div>
        );
      })}

    </div>
  );
}

export default AgentActivity;
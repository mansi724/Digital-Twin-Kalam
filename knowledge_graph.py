# knowledge_graph.py
# Builds and visualizes a live knowledge graph
# showing how topics in conversation are connected

import json
import os
from google import genai
from dotenv import load_dotenv
from pyvis.network import Network

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ─────────────────────────────────────────
# EXTRACT ENTITIES AND RELATIONSHIPS
# ─────────────────────────────────────────

def extract_entities(text):
    """
    Uses Gemini to extract key entities and relationships
    from a conversation turn.
    Returns a dict with nodes and edges.
    """
    prompt = f"""
Extract key entities and relationships from this text about Dr. APJ Abdul Kalam.

Text: {text[:500]}

Return ONLY a valid JSON object like this example:
{{
    "nodes": [
        {{"id": "Rameswaram", "type": "place"}},
        {{"id": "ISRO", "type": "organization"}},
        {{"id": "Agni Missile", "type": "project"}}
    ],
    "edges": [
        {{"from": "Kalam", "to": "ISRO", "label": "worked at"}},
        {{"from": "Kalam", "to": "Agni Missile", "label": "developed"}}
    ]
}}

Types can be: person, place, organization, project, concept, book, event
Keep it to maximum 5 nodes and 4 edges.
Return ONLY the JSON, no explanation.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        # Clean response and parse JSON
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        return {"nodes": [], "edges": []}


# ─────────────────────────────────────────
# KNOWLEDGE GRAPH CLASS
# ─────────────────────────────────────────

class KnowledgeGraph:

    def __init__(self):
        self.nodes = {}  # id -> type
        self.edges = []  # list of (from, to, label)

        # Always add Kalam as center node
        self.nodes["Dr. Kalam"] = "person"

    def update(self, user_message, bot_response):
        """
        Updates graph with new entities from conversation.
        """
        # Extract from both user message and bot response
        combined = f"{user_message} {bot_response}"
        extracted = extract_entities(combined)

        # Add new nodes
        for node in extracted.get("nodes", []):
            node_id = node.get("id", "")
            node_type = node.get("type", "concept")
            if node_id and node_id not in self.nodes:
                self.nodes[node_id] = node_type

        # Add new edges
        for edge in extracted.get("edges", []):
            from_node = edge.get("from", "")
            to_node = edge.get("to", "")
            label = edge.get("label", "")

            if from_node and to_node:
                # Avoid duplicate edges
                if not any(e[0] == from_node and e[1] == to_node
                          for e in self.edges):
                    self.edges.append((from_node, to_node, label))

    def render(self, output_path="memory/knowledge_graph.html"):
        """
        Renders the knowledge graph as an interactive HTML file.
        """
        if len(self.nodes) <= 1:
            return None

        # Color map for node types
        color_map = {
            "person":       "#FFD700",
            "place":        "#64ff96",
            "organization": "#64c8ff",
            "project":      "#ff9f43",
            "concept":      "#a29bfe",
            "book":         "#fd79a8",
            "event":        "#81ecec"
        }

        # Create network
        net = Network(
            height="400px",
            width="100%",
            bgcolor="#0a0a1a",
            font_color="white",
            directed=True
        )

        net.set_options("""
        {
            "nodes": {
                "font": {"size": 12, "color": "white"},
                "borderWidth": 2,
                "shadow": true
            },
            "edges": {
                "color": {"color": "#444466"},
                "font": {"size": 9, "color": "#a0a0c0"},
                "smooth": {"type": "curvedCW"}
            },
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -50,
                    "springLength": 100
                },
                "solver": "forceAtlas2Based"
            }
        }
        """)

        # Add nodes
        for node_id, node_type in self.nodes.items():
            color = color_map.get(node_type, "#a29bfe")
            size = 25 if node_id == "Dr. Kalam" else 15
            net.add_node(
                node_id,
                label=node_id,
                color=color,
                size=size,
                title=f"Type: {node_type}"
            )

        # Add edges
        for from_node, to_node, label in self.edges:
            if from_node in self.nodes and to_node in self.nodes:
                net.add_edge(from_node, to_node, title=label, label=label)

        # Save to file
        os.makedirs("memory", exist_ok=True)
        net.save_graph(output_path)
        return output_path

    def get_stats(self):
        """Returns basic stats about the graph."""
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "topics": [n for n, t in self.nodes.items()
                      if t in ["concept", "project", "event"]]
        }
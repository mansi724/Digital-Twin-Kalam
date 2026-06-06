# embedding_visualizer.py
# Visualizes user questions and Kalam's knowledge chunks
# in 2D embedding space using UMAP + Plotly

import numpy as np
import plotly.graph_objects as go
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

# ─────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────

# Use same model as RAG pipeline
model = SentenceTransformer("all-MiniLM-L6-v2")

# ─────────────────────────────────────────
# EMBEDDING VISUALIZER CLASS
# ─────────────────────────────────────────

class EmbeddingVisualizer:

    def __init__(self):
        self.user_questions = []      # List of user questions
        self.bot_responses = []       # List of bot responses
        self.all_texts = []           # All texts combined
        self.all_labels = []          # Labels for each text
        self.all_types = []           # Types: "question" or "response"

    def add_turn(self, user_message, bot_response):
        """
        Adds a conversation turn to the visualizer.
        """
        self.user_questions.append(user_message[:100])
        self.bot_responses.append(bot_response[:100])

        self.all_texts.append(user_message[:100])
        self.all_labels.append(f"Q: {user_message[:30]}...")
        self.all_types.append("question")

        self.all_texts.append(bot_response[:100])
        self.all_labels.append(f"A: {bot_response[:30]}...")
        self.all_types.append("response")

    def render(self):
        """
        Renders the embedding space as an interactive Plotly chart.
        Returns a Plotly figure.
        """
        if len(self.all_texts) < 4:
            return None

        # ── Generate embeddings ──
        embeddings = model.encode(self.all_texts)

        # ── Reduce to 2D using PCA ──
        # PCA is faster than UMAP and works well for small datasets
        n_components = min(2, len(self.all_texts) - 1)
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(embeddings)

        # ── Separate questions and responses ──
        q_x, q_y, q_labels = [], [], []
        r_x, r_y, r_labels = [], [], []

        for i, (x, y) in enumerate(reduced):
            if self.all_types[i] == "question":
                q_x.append(x)
                q_y.append(y)
                q_labels.append(self.all_labels[i])
            else:
                r_x.append(x)
                r_y.append(y)
                r_labels.append(self.all_labels[i])

        # ── Build Plotly figure ──
        fig = go.Figure()

        # User questions — blue dots
        fig.add_trace(go.Scatter(
            x=q_x, y=q_y,
            mode="markers+text",
            name="Your Questions",
            text=q_labels,
            textposition="top center",
            marker=dict(
                size=12,
                color="#64c8ff",
                symbol="circle",
                line=dict(color="#ffffff", width=1)
            ),
            textfont=dict(size=9, color="#64c8ff")
        ))

        # Bot responses — gold dots
        fig.add_trace(go.Scatter(
            x=r_x, y=r_y,
            mode="markers+text",
            name="Kalam's Responses",
            text=r_labels,
            textposition="bottom center",
            marker=dict(
                size=12,
                color="#FFD700",
                symbol="diamond",
                line=dict(color="#ffffff", width=1)
            ),
            textfont=dict(size=9, color="#FFD700")
        ))

        # Draw lines connecting question to response pairs
        for i in range(min(len(q_x), len(r_x))):
            fig.add_trace(go.Scatter(
                x=[q_x[i], r_x[i]],
                y=[q_y[i], r_y[i]],
                mode="lines",
                line=dict(color="rgba(255,255,255,0.1)", width=1, dash="dot"),
                showlegend=False,
                hoverinfo="skip"
            ))

        # ── Style the figure ──
        fig.update_layout(
            title=dict(
                text="🗺️ Embedding Space — Where questions land in Kalam's knowledge",
                font=dict(color="white", size=13)
            ),
            paper_bgcolor="#0a0a1a",
            plot_bgcolor="#0d1117",
            font=dict(color="white"),
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.05)",
                zeroline=False,
                showticklabels=False,
                title="Semantic Dimension 1"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.05)",
                zeroline=False,
                showticklabels=False,
                title="Semantic Dimension 2"
            ),
            legend=dict(
                bgcolor="rgba(255,255,255,0.05)",
                bordercolor="rgba(255,255,255,0.1)",
                borderwidth=1
            ),
            height=400,
            margin=dict(l=40, r=40, t=60, b=40)
        )

        return fig
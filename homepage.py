import streamlit as st

st.set_page_config(page_title="USG Sizing Tools", page_icon="⚙️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f1117;
}

[data-testid="stAppViewContainer"] {
    background: #0f1117;
}

[data-testid="stHeader"] {
    background: transparent;
}

.main-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 3.2rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #ffffff;
    margin-bottom: 0.1em;
    line-height: 1;
}

.main-subtitle {
    font-family: 'Barlow', sans-serif;
    font-weight: 300;
    font-size: 1rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 3rem;
}

.divider {
    border: none;
    border-top: 1px solid #1f2937;
    margin: 2rem 0;
}

.section-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 1.2rem;
}

.tool-card {
    display: block;
    text-decoration: none;
    background: #161b27;
    border: 1px solid #1f2937;
    border-radius: 4px;
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.tool-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: #e85d26;
    transform: scaleY(0);
    transition: transform 0.2s ease;
    transform-origin: bottom;
}

.tool-card:hover {
    border-color: #374151;
    background: #1a2030;
    transform: translateX(4px);
    text-decoration: none;
}

.tool-card:hover::before {
    transform: scaleY(1);
}

.tool-card.featured {
    border-color: #2d3748;
    background: #1a2030;
    padding: 2rem 2rem;
}

.tool-card.featured::before {
    transform: scaleY(1);
    background: #e85d26;
}

.card-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 1.5rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #f9fafb;
    margin-bottom: 0.3rem;
}

.card-title.featured-title {
    font-size: 1.9rem;
    color: #ffffff;
}

.card-desc {
    font-family: 'Barlow', sans-serif;
    font-weight: 400;
    font-size: 0.875rem;
    color: #6b7280;
    line-height: 1.5;
    margin: 0;
}

.card-arrow {
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    color: #374151;
    font-size: 1.2rem;
    transition: all 0.2s ease;
}

.tool-card:hover .card-arrow {
    color: #e85d26;
    transform: translateY(-50%) translateX(3px);
}

.beta-badge {
    display: inline-block;
    font-family: 'Barlow', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #e85d26;
    border: 1px solid #e85d26;
    border-radius: 2px;
    padding: 0.1rem 0.4rem;
    margin-left: 0.6rem;
    vertical-align: middle;
    position: relative;
    top: -2px;
}

.footer {
    font-family: 'Barlow', sans-serif;
    font-size: 0.75rem;
    color: #374151;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>

<div style="padding: 2rem 0 1rem 0;">
    <div class="main-title">USG Sizing Tools</div>
    <div class="main-subtitle">Gas Regulator Selection & Sizing</div>
</div>

<hr class="divider">

<div class="section-label">Featured</div>

<a class="tool-card featured" href="https://allmodels-usg.streamlit.app/" target="_blank">
    <div class="card-title featured-title">
        All Models <span class="beta-badge">Beta</span>
    </div>
    <p class="card-desc">Sizes across the full regulator lineup. Recommended starting point — automatically selects the best model for your application.</p>
    <span class="card-arrow">→</span>
</a>

<hr class="divider">

<div class="section-label">Model-Specific Tools</div>

<a class="tool-card" href="https://model496-usg.streamlit.app/" target="_blank">
    <div class="card-title">Model 496</div>
    <p class="card-desc">Low-pressure service regulator. Inlet 1–125 psi · Outlet 3.5" wc – 2 psi</p>
    <span class="card-arrow">→</span>
</a>

<a class="tool-card" href="https://model143-usg.streamlit.app/" target="_blank">
    <div class="card-title">Model 143</div>
    <p class="card-desc">Medium-pressure service regulator. Inlet 0.5–125 psi · Outlet 3.5" wc – 6 psi</p>
    <span class="card-arrow">→</span>
</a>

<div class="footer">United Sales Group &nbsp;·&nbsp; Regulator Sizing Platform</div>
""", unsafe_allow_html=True)

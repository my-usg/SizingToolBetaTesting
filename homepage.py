import streamlit as st

st.set_page_config(page_title="USG Sizing Tools", page_icon="⚙️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #111827;
}

[data-testid="stAppViewContainer"] {
    background: #ffffff;
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
    color: #111827;
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
    color: #9ca3af;
    margin-bottom: 1.2rem;
}

.tool-card {
    display: block;
    text-decoration: none;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
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
    border-color: #d1d5db;
    background: #f3f4f6;
    transform: translateX(4px);
    text-decoration: none;
}

.tool-card:hover::before {
    transform: scaleY(1);
}

.tool-card.featured {
    border-color: #e5e7eb;
    background: #f3f4f6;
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
    color: #111827;
    margin-bottom: 0.3rem;
}

.card-title.featured-title {
    font-size: 1.9rem;
    color: #111827;
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
    color: #d1d5db;
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
    color: #d1d5db;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>

<div style="padding: 2rem 0 1rem 0;">
    <div class="main-title">Sizing Tool <span class="beta-badge">Beta</span></div>
    </div>

<hr class="divider">

<a class="tool-card featured" href="https://allmodels-usg.streamlit.app/" target="_blank">
    <div class="card-title featured-title">All Models <span class="beta-badge">Beta</span></div>
    <span class="card-arrow">→</span>
</a>
            
<a class="tool-card" href="https://configurator-usg.streamlit.app/" target="_blank">
    <div class="card-title">Part Number Configurator <span class="beta-badge">Beta</span></div>
    <span class="card-arrow">→</span>
</a>
            
<a class="tool-card" href="https://model461-usg.streamlit.app/" target="_blank">
    <div class="card-title">Model 441/461 <span class="beta-badge">Beta</span></div>
    <span class="card-arrow">→</span>
</a>
            
<a class="tool-card" href="https://model243-usg.streamlit.app/" target="_blank">
    <div class="card-title">Model 243 <span class="beta-badge">Beta</span></div>
    <span class="card-arrow">→</span>
</a>

<a class="tool-card" href="https://model046-usg.streamlit.app/" target="_blank">
    <div class="card-title">Model 046 <span class="beta-badge">Beta</span></div>
    <span class="card-arrow">→</span>
</a>
            
<a class="tool-card" href="https://model143-usg.streamlit.app/" target="_blank">
    <div class="card-title">Model 143 <span class="beta-badge">Beta</span></div>
    <span class="card-arrow">→</span>
</a>
            
<a class="tool-card" href="https://model496-usg.streamlit.app/" target="_blank">
    <div class="card-title">Model 496 <span class="beta-badge">Beta</span></div>
    <span class="card-arrow">→</span>
</a>

<a class="tool-card" href="https://model121-usg.streamlit.app/" target="_blank">
    <div class="card-title">Model 121/122 <span class="beta-badge">Beta</span></div>
    <span class="card-arrow">→</span>
</a>

<div class="footer">United Sales Group &nbsp;·&nbsp; Regulator Sizing Platform</div>
""", unsafe_allow_html=True)
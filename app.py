import streamlit as st
import joblib
import os

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Phishing Detection System",
    page_icon="🔐",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
body { background-color: #0e1117; }
.main { background-color: #0e1117; color: white; }

.title {
    text-align: center;
    font-size: 40px;
    color: #00ffcc;
    font-weight: bold;
    margin-bottom: 5px;
}
.subtitle {
    text-align: center;
    color: #8b9ab0;
    font-size: 15px;
    margin-bottom: 30px;
}
.badge {
    display: inline-block;
    background: #1a2030;
    border: 1px solid #00ffcc33;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    color: #00ffcc;
    margin: 2px;
}
.result-danger {
    padding: 18px 20px;
    border-radius: 12px;
    background: linear-gradient(135deg, #3d1111, #5a1a1a);
    border-left: 4px solid #ff4b4b;
    color: #ff6b6b;
    font-size: 22px;
    font-weight: bold;
    margin: 10px 0;
}
.result-safe {
    padding: 18px 20px;
    border-radius: 12px;
    background: linear-gradient(135deg, #0d2b1d, #1a3d2b);
    border-left: 4px solid #00ff99;
    color: #00ff99;
    font-size: 22px;
    font-weight: bold;
    margin: 10px 0;
}
.metric-box {
    background: #1a2030;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 6px 0;
    border: 1px solid #2a3040;
}
.tip-item {
    background: #1a2030;
    border-left: 3px solid #00ffcc;
    padding: 8px 12px;
    margin: 5px 0;
    border-radius: 0 8px 8px 0;
    font-size: 13px;
    color: #cfcfcf;
}
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────
@st.cache_resource
def load_model():
    if not os.path.exists("phishing_model.pkl"):
        st.error("❌ Model not found! Run: python train_model.py first.")
        st.stop()
    model = joblib.load("phishing_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="title">🔐 AI Phishing Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Detect malicious emails using Machine Learning + NLP</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<span class="badge">🤖 Logistic Regression</span>', unsafe_allow_html=True)
with col2:
    st.markdown('<span class="badge">📊 TF-IDF NLP</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="badge">🛡️ Real-time Analysis</span>', unsafe_allow_html=True)

st.markdown("---")

# ── Main Input ────────────────────────────────────────────────
st.subheader("📩 Email Content Analyzer")

email_text = st.text_area(
    "Paste suspicious email content below:",
    height=180,
    placeholder="Example: Urgent! Your account has been suspended. Click here to verify immediately..."
)

# Quick test examples
st.markdown("**⚡ Quick Test Examples:**")
ex_col1, ex_col2 = st.columns(2)
with ex_col1:
    if st.button("🔴 Test Phishing Email"):
        st.session_state["sample"] = "Urgent! Your bank account is suspended. Verify your password immediately to restore access."
with ex_col2:
    if st.button("🟢 Test Legitimate Email"):
        st.session_state["sample"] = "Hi team, the project report is attached. Please review and share your feedback by Friday."

if "sample" in st.session_state:
    email_text = st.session_state["sample"]
    st.info(f"📋 Sample loaded: *{email_text[:60]}...*")

# ── Analyze Button ────────────────────────────────────────────
if st.button("🔍 Analyze Email", use_container_width=True):

    if not email_text.strip():
        st.warning("⚠️ Please enter or paste email content first.")
    else:
        with st.spinner("🔄 Running ML analysis..."):

            transformed = vectorizer.transform([email_text])
            prediction = model.predict(transformed)[0]
            probability = model.predict_proba(transformed)[0]

            phishing_conf = round(probability[1] * 100, 2)
            safe_conf = round(probability[0] * 100, 2)

        st.markdown("---")
        st.subheader("📊 Detection Result")

        if prediction == 1:
            st.markdown(
                '<div class="result-danger">⚠️ PHISHING EMAIL DETECTED</div>',
                unsafe_allow_html=True
            )
            st.error(f"🚨 Threat Confidence: **{phishing_conf}%**")
            st.progress(int(phishing_conf))

            st.markdown("**🔍 Risk Indicators Found:**")
            keywords = ["urgent", "verify", "suspend", "click", "password", "account", "immediately", "free", "win", "claim", "otp", "bank"]
            found = [kw for kw in keywords if kw.lower() in email_text.lower()]
            if found:
                st.markdown(f"🔴 Suspicious keywords: `{'`, `'.join(found)}`")

        else:
            st.markdown(
                '<div class="result-safe">✅ EMAIL LOOKS LEGITIMATE</div>',
                unsafe_allow_html=True
            )
            st.success(f"✔️ Safety Confidence: **{safe_conf}%**")
            st.progress(int(safe_conf))

        # Confidence metrics
        st.markdown("---")
        st.subheader("📈 Confidence Breakdown")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("🔴 Phishing Score", f"{phishing_conf}%")
        with m2:
            st.metric("🟢 Legitimate Score", f"{safe_conf}%")

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.markdown("## 🛡️ Cyber Awareness")
st.sidebar.markdown("---")

tips = [
    "🔗 Never click suspicious links",
    "👤 Verify sender identity",
    "🔢 Never share OTPs with anyone",
    "🔐 Use strong unique passwords",
    "📱 Enable 2-Factor Authentication",
    "📧 Check sender email domain carefully",
    "⚠️ Urgency is a red flag — take your time",
    "🏦 Banks never ask for passwords via email",
]
for tip in tips:
    st.sidebar.markdown(f'<div class="tip-item">{tip}</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**🧠 How it works:**")
st.sidebar.markdown("""
1. Email text is vectorized using **TF-IDF**
2. **Logistic Regression** predicts class
3. Confidence score is calculated
4. Risk keywords are highlighted
""")

# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.caption("🔐 AI Phishing Detection System | Built for cybersecurity awareness | Educational purposes only")
st.caption("👩‍💻 Author: Hepisha | Cyber Hepisha")

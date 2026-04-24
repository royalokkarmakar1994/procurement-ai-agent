# 🏭 Procurement AI Agent

An intelligent procurement decision-support tool that scores vendors using weighted criteria and generates AI-powered recommendations using LangChain and OpenAI GPT.

Built to demonstrate the practical application of LLMs in supply chain and procurement workflows.

---

## 🚀 What It Does

1. **Loads vendor data** — from a CSV upload or built-in sample dataset
2. **Scores vendors automatically** — using a configurable weighted scoring model (price, delivery, quality, reliability, payment terms, dispute history)
3. **Generates AI recommendations** — sends the top vendors to GPT via LangChain for a structured procurement recommendation including primary choice, backup vendor, risk assessment, and negotiation tips

---

## 🖥️ Demo

> *(Add a screenshot or screen recording GIF here after running the app)*

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **Streamlit** | Interactive web UI |
| **Pandas** | Vendor data processing and scoring |
| **LangChain** | LLM orchestration and prompt chaining |
| **OpenAI GPT-3.5** | Natural language recommendation engine |

---

## 📁 Project Structure

```
procurement-ai-agent/
├── app.py              ← Streamlit frontend
├── scorer.py           ← Weighted vendor scoring engine
├── agent.py            ← LangChain + OpenAI recommendation agent
├── data/
│   └── vendors.csv     ← Sample vendor dataset
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/procurement-ai-agent.git
cd procurement-ai-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Enter your OpenAI API key in the sidebar and click **Generate Recommendation**

---

## 📊 Scoring Model

Each vendor is scored on six criteria, normalized to a 0–10 scale:

| Criterion | Weight | Direction |
|---|---|---|
| Unit Price | 30% | Lower is better |
| Delivery Time | 25% | Fewer days is better |
| Quality Score | 20% | Higher is better |
| Reliability Score | 15% | Higher is better |
| Payment Terms | 7% | Longer terms are better |
| Past Disputes | 3% | Fewer is better |

Weights are fully configurable in `scorer.py`.

---

## 💡 Why I Built This

With a background in supply chain operations at Tata Steel and TCS, I've seen how vendor selection decisions are often made manually, inconsistently, and without structured data. This project demonstrates how LLMs can augment that process — not replace human judgment, but structure it and surface insights faster.

---

## 🔮 Future Improvements

- [ ] Add multi-category procurement support (raw materials vs. services)
- [ ] Integrate with ERP APIs (SAP, Oracle) for live vendor data
- [ ] Add historical procurement trend analysis
- [ ] Fine-tune LLM on domain-specific procurement data

---

## 📬 Contact

**Alok** — AI Collaborator | Prompt Engineer  
[LinkedIn](https://linkedin.com/in/YOUR_PROFILE) · [GitHub](https://github.com/YOUR_USERNAME)

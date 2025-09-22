# 🧪 Snowcrash — Offensive LLM Red-Teaming Framework

<p align="center">
  <img src="https://res.cloudinary.com/dsqufr1x5/image/upload/v1758358647/snowcrash_litukz.jpg" alt="Snowcrash Logo" width="800"/>
</p>

**Snowcrash** is an **offensive-first LLM red-teaming platform** that automates adversarial testing of large language models, AI agents, and Model Context Protocol (MCP) tools.  
It simulates real-world attack chains, uncovers vulnerabilities, and generates reproducible evidence packs — empowering enterprises, governments, and researchers to secure AI before adversaries exploit it.  

---

## ⚡ Features

- 🔴 **Offensive-first** — built by red-teamers, for red-teamers.  
- 🛠️ **Scenario Builder** — design multi-step adversarial chains, jailbreaks, tool abuse, and policy bypasses.  
- 🔌 **Target Config** — connect LLMs (OpenAI, Anthropic, open-source models), AI agents, and MCP tools.  
- 🚀 **Campaign Runner** — simulate adversary operations at scale with budgeted attack paths.  
- 📊 **Findings Dashboard** — severity-based vulnerability triage with evidence trails.  
- 📁 **Evidence & Reporting** — export reproducible adversarial traces, compliance-ready.  
- 🛡️ **Continuous Assurance** — automate recurring red-team runs as part of CI/CD pipelines.  

---

## 🎯 Why Snowcrash?

🔐 **AI is the new attack surface.**  
Snowcrash uncovers:  
- Prompt injections & role jailbreaks  
- Tool abuse (MCP escalation, filesystem/browser/DB exfiltration)  
- PII and secrets leakage  
- Data poisoning vectors  
- Policy bypasses & compliance gaps  

Unlike traditional security tools, Snowcrash is:  
- ⚔️ **Offensive-first** — assumes breach, simulates adversary workflows.  
- 🔄 **Automated** — continuous adversarial testing instead of one-off audits.  
- 🧩 **Composable** — plug into any AI stack (LangChain, LlamaIndex, vLLM, Anthropic, OpenAI, etc.).  

---

## 🖥️ UI Preview

<video width="100%" controls muted>
  <source src="https://res.cloudinary.com/dsqufr1x5/video/upload/v1758537520/2025-09-22_16-01-06_sw72px.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## 🚀 Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/your-org/snowcrash.git
cd snowcrash
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit UI
```bash
streamlit run app.py
```

### 4. Open your browser
Navigate to [http://localhost:8501](http://localhost:8501) to access the Snowcrash dashboard.  

---

## 📂 Project Structure
```
snowcrash/
│── app.py                # Streamlit UI
│── core/                 # Core adversarial engine
│── scenarios/            # Attack scenario templates
│── findings/             # Evidence & reports
│── docs/                 # Documentation & guides
│── tests/                # Unit & integration tests
```

---

## 📊 Roadmap

- [ ] LLM Jailbreak scenario packs  
- [ ] Advanced MCP tool abuse simulations  
- [ ] Integration with SIEM / SOC platforms  
- [ ] SaaS dashboard with multi-tenant support  
- [ ] Compliance automation (FedRAMP, SOC2, HIPAA)  

---

## 🤝 Contributing

We welcome offensive security researchers, AI engineers, and policy experts to contribute.  
1. Fork the repo  
2. Create a branch (`git checkout -b feature/amazing`)  
3. Commit changes (`git commit -m 'Added amazing feature'`)  
4. Push (`git push origin feature/amazing`)  
5. Open a Pull Request  

---

## 🛡️ Disclaimer

Snowcrash is an **offensive security tool**. Use only on systems you own or have explicit permission to test.  
The maintainers are **not responsible for misuse** of this software.  

---

## ⭐ Support & Community

- 🐦 Twitter: [@snowcrashsec](https://twitter.com/snowcrashsec)  
- 💬 Discord: [Join the community](https://discord.gg/your-invite)  
- 📧 Contact: security@snowcrash.io  

If you like this project, consider giving it a **⭐ star** — it helps us grow the community!  

---

🔥 Snowcrash — *Because every LLM is an attack surface.*  

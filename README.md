# AI Research & Analytics Agent

An AI-powered research and data analytics application that helps users explore datasets, generate meaningful insights, visualize data, and retrieve research information through an interactive web interface.

## 🚀 Project Overview

The AI Research & Analytics Agent combines data analytics with AI-powered research capabilities. Users can ask questions, analyze structured datasets, explore visualizations, and obtain research-oriented responses with citations.

The project aims to simplify data exploration and research by bringing multiple analytical capabilities into one application.

## ✨ Key Features

* **Dataset Analysis:** Process and analyze structured datasets.
* **Automated Insights:** Generate data-grounded findings from analytical results.
* **Interactive Visualizations:** Select suitable charts based on the user's question and available data.
* **AI-Powered Research:** Retrieve relevant research information and provide citation-supported responses.
* **RAG-Based Retrieval:** Use Retrieval-Augmented Generation to support research question answering.
* **Interactive Dashboard:** Explore the application through a Streamlit interface.
* **Online Deployment:** Access the application through Streamlit Community Cloud.

## 🛠️ Technologies Used

* Python
* Pandas and NumPy
* Matplotlib and Plotly
* Streamlit
* LangGraph
* Google Gemini API
* Retrieval-Augmented Generation (RAG)
* arXiv and Semantic Scholar
* pytest

## 🏗️ System Workflow

1. The user submits a research question or dataset.
2. The application processes the input and identifies the required analysis.
3. Data processing and analytical components generate structured results.
4. The agent selects appropriate visualizations and derives insights from the results.
5. Research queries retrieve relevant papers and supporting citations.
6. The application presents the results through an interactive dashboard.

## 📂 Project Structure

```text
AI-Research-Agent/
├── app/
│   ├── streamlit_app.py
│   └── agent_runner.py
├── src/
│   └── agents/
│       ├── dashboard_model.py
│       └── ...
├── tests/
├── data/
├── requirements.txt
├── .env.example
└── README.md
```

*Note: This is a simplified overview of the repository structure.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/psmrithi/AI-Research-Agent.git
cd AI-Research-Agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Add your own valid API key and the configuration required by the application.

**Important:** Never upload your `.env` file or expose API keys in your repository.

### 5. Run the application

```bash
python -m streamlit run app/streamlit_app.py
```

Open the local URL displayed in your terminal.

## 🧪 Testing

Run the project's test suite with:

```bash
python -m pytest -v
```

## 🌐 Live Demo

**Live Application:** [Open AI Research & Analytics Agent](PASTE_YOUR_STREAMLIT_URL_HERE)

## 💻 Source Code

**GitHub Repository:** https://github.com/psmrithi/AI-Research-Agent

## 🎯 Learning Outcomes

* Practical experience with Python-based data analytics.
* Understanding of AI agents and workflow orchestration.
* Experience with Retrieval-Augmented Generation.
* Data visualization and automated insight generation.
* API integration and environment configuration.
* Application testing and cloud deployment.

## 🔮 Future Improvements

* Support for additional dataset formats.
* More advanced analytical methods and visualizations.
* Improved research retrieval and citation evaluation.
* Enhanced dashboard customization.
* More robust error handling and performance optimization.

## 👩‍💻 Author

**Smrithi**

GitHub: [psmrithi](https://github.com/psmrithi)

---

*Built to explore the intersection of artificial intelligence, research, and data analytics.*

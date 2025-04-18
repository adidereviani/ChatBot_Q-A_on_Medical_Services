# 📄 ChatBot_Q-A_on_Medical_Services

An AI-powered, multilingual (Hebrew and English) **stateless microservice chatbot** that collects personal medical information and provides **personalized Q&A** about services offered by Israeli HMOs: **Maccabi**, **Meuhedet**, and **Clalit**. All user session data is managed on the client side (frontend).

Built using **FastAPI**, **Streamlit**, and **Azure OpenAI**, connected to a local database of medical service benefits extracted from HTML files.

---

## 📂 Project Structure

```plaintext
ChatBot_Q-A_on_Medical_Services/
├── backend/
│   ├── app/
│   │   ├── data/
│   │   │   └── phase2_data/
│   │   │       ├── alternative_services.html
│   │   │       ├── communication_clinic_services.html
│   │   │       ├── dentel_services.html
│   │   │       ├── optometry_services.html
│   │   │       ├── pragrency_services.html
│   │   │       └── workshops_services.html
│   │   ├── services/
│   │   │   ├── confirm_classifier.py
│   │   │   ├── info_collector.py
│   │   │   ├── llm_client.py
│   │   │   ├── qa_handler.py
│   │   │   └── user_info_extractor.py
│   │   ├── utils/
│   │   │   ├── html_loader.py
│   │   │   ├── logger.py
│   │   │   ├── test_concurrency.py
│   │   │   └── test_html_read.py
│   │   ├── api.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── README.md
└── .env
```

---

## ⚙️ How It Works

1. **User starts a chat** via Streamlit.
2. **Info Collection Phase** (`phase = info_collection`)
   - Bot asks personal details (name, ID, gender, etc.).
   - Bot **prints a clear confirmation summary**.
   - If user confirms ➔ switches to QA phase.
3. **Question Answering Phase** (`phase = qa`)
   - Bot answers based on user HMO/tier from loaded HTML knowledge base.
4. **Logging**:  
   - All messages and interactions are saved in `chatbot.log`.
5. **Data Source**:  
   - Local HTML files parsed via `BeautifulSoup`.

---

## 🛠️ Technologies Used

- **FastAPI** — API server.
- **Streamlit** — Web UI.
- **Azure OpenAI** — LLM completion service.
- **BeautifulSoup** — HTML parsing for knowledge base.
- **httpx / asyncio** — Async concurrency for testing.
- **Pydantic** — Payload validation.

---

## 📦 Installation

### 1. Clone the project
```bash
git clone https://github.com/adidereviani/ChatBot_Q-A_on_Medical_Services.git
cd ChatBot_Q-A_on_Medical_Services
```

### 2. Install Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend
```bash
cd ../frontend
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create `.env` file inside `/backend/` folder:
```
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_API_VERSION=your-api-version
AZURE_OPENAI_API_BASE=https://your-resource-name.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your-deployment-name
```

---

## 🚀 Running Locally

### Start backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

### Start frontend (Streamlit app):
```bash
cd frontend
streamlit run app.py
```

Visit [http://localhost:8501](http://localhost:8501) to interact with the chatbot.

---

## 🌐 Language Support

- **English** 🇬🇧
- **עברית (Hebrew)** 🇮🇱

Select your preferred language.

---
## ✨ Features

- Multilingual conversation (Hebrew / English).
- Phase switching: `info_collection` ➔ `qa`.
- Integration with Azure OpenAI GPT.
- Auto-recovery if user info is missing or incomplete.
- Fully logged conversation history.
- Local database of insurance services parsed from HTML.


---

## 👨‍💻 Author

Developed by Adi Prager.

---

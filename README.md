# 🤖 Math Homework Assistant with AI Guardrails

This project is a demonstration of how to build a **guardrail-protected AI assistant** using the `agents` framework and OpenAI-compatible models (like **Gemini 2.5 Flash**). It applies both **input** and **output** guardrails to manage allowed content in a user query and model response.

--- 
  
## 📌 Features    

- ✅ Detects whether a user query is related to **math** (Input Guardrail)
- ⚠️ Flags or blocks **political content** in responses (Output Guardrail)
- 🧠 Uses Gemini 2.5 Flash model with OpenAI-compatible interface
- 🚦 Integrated guardrail architecture using `agents`
- 🔐 Environment-configured API keys and base URLs

---

## 🏗️ How It Works

1. **Input Guardrail** checks if the user's question is related to math.
2. If **not math-related**, the agent proceeds, but the input can still be flagged.
3. **Output Guardrail** checks if the response is **politically related**.
4. If **politics is detected**, it raises a `OutputGuardrailTripwireTriggered`.

---

## 🧪 Example Usage

**Query**: `"TELL ME politcain zulfikar ali bhutto"`

**Flow**:

- ✅ Passes input check (not a math question)
- ❌ Fails output check (contains political content)
- ⚠️ Triggers Output Guardrail

---

## 💻 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name










# 🧠 Daily Mood Tracker

An AI-powered mood journaling application built with Streamlit and Groq that helps users track their emotions, receive personalized insights, and visualize mood trends over time.

Users can write about their day in natural language, and the application automatically analyzes their emotional state using a Large Language Model (LLM), generates a concise summary, and provides an encouraging Islamic reminder.

---

🚀 Live Demo: https://aidailymoodtracker.streamlit.app/

## 📸 Application Preview
<img width="2876" height="1722" alt="image" src="https://github.com/user-attachments/assets/7bd685fe-fdb9-4266-8c79-3a5e2a143855" />
<img width="2876" height="1722" alt="image" src="https://github.com/user-attachments/assets/6bc51b3e-57dd-4a26-b99f-7743d4a71e60" />
<img width="2876" height="600" alt="image" src="https://github.com/user-attachments/assets/4e7925a4-36a0-4b01-bb55-977dec998818" />
<img width="2876" height="664" alt="image" src="https://github.com/user-attachments/assets/88cfd4bd-fefd-4a06-99fd-e9dbcea2e2d4" />

---

## 🚀 Features

### ✍️ Mood Journal Entry

* Write daily thoughts and feelings in natural language.
* Submit entries through an intuitive Streamlit interface.

### 🤖 AI Mood Analysis

Powered by Groq's Llama 3.3 70B model:

* Detects the user's mood automatically.
* Generates a short summary of the entry.
* Provides an Islamic reminder or motivational suggestion.

### 📊 Mood Analytics Dashboard

Visualize emotional patterns over time:

* Mood distribution chart
* Daily mood entry trends
* Most frequent mood in the last 7 days
* Most frequent mood in the last 30 days

### 🗂️ Data Management

* Stores mood entries locally in JSON format.
* Displays all historical entries in a searchable table.

---

## 🏗️ Project Structure

```bash
Daily-Mood-Tracker/
│
├── app.py               # Main Streamlit application
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation
```

---

## 🧠 How It Works

1. User writes a journal entry.
2. The text is sent to Groq's Llama 3.3 70B model.
3. The model extracts:

   * Mood
   * Summary
   * Islamic suggestion
4. The result is stored in a JSON database.
5. Analytics are generated using Pandas and Matplotlib.
6. Users can view trends and emotional patterns over time.

---

## 🛠️ Tech Stack

| Technology              | Purpose                        |
| ----------------------- | ------------------------------ |
| Python                  | Core programming language      |
| Streamlit               | Web application framework      |
| Groq API                | LLM-powered mood analysis      |
| Llama 3.3 70B Versatile | Natural language understanding |
| Pandas                  | Data processing and analytics  |
| Matplotlib              | Data visualization             |
| JSON                    | Local data storage             |

---

## 📈 Analytics Included

### Mood Distribution

Displays the percentage breakdown of detected moods across all entries.

### Mood Timeline

Shows how frequently entries were logged over time.

### Trend Analysis

Tracks:

* Most common mood in the last 7 days
* Most common mood in the last 30 days

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/daily-mood-tracker.git
cd daily-mood-tracker
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variable

Set your Groq API key:

```bash
export GROQ_API_KEY="your_api_key"
```

For Windows:

```bash
set GROQ_API_KEY=your_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will launch in your browser at:

```bash
http://localhost:8501
```

---

## Example Workflow

### User Input

```text
I've been feeling overwhelmed with assignments lately, but I'm trying my best to stay productive.
```

### AI Output

**Mood:** Stressed

**Summary:** The user feels overwhelmed by academic responsibilities but remains motivated.

**Suggestion:** Trust Allah's plan, remain patient, and continue striving with sincerity.

---

## Future Improvements

* User authentication
* Cloud database integration
* Mood streak tracking
* Export mood reports
* Sentiment score visualization
* Weekly AI-generated mental wellness summaries
* Personalized recommendations

---

## Learning Outcomes

This project demonstrates:

* Prompt engineering
* LLM integration using APIs
* Streamlit application development
* Data visualization
* JSON data handling
* Building AI-powered productivity and wellness tools

---

## Author

**Ayesha Tariq**

Aspiring AI Engineer, Builder of purpose-driven technology.

---

## License

This project is open-source and available under the MIT License.

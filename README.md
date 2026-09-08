# FairSplit AI 🧾

FairSplit AI is a smart bill-splitting web application built with **Python and Streamlit**. It uses **Google Gemini AI** to analyze uploaded bills, extract food items and prices, and assign individual items to friends so everyone pays exactly for what they consumed.

## 🚀 Features

* 📸 Upload a bill image
* 🤖 AI-powered bill analysis using Google Gemini
* 🧾 Extract food items and their prices
* 👥 Add multiple friends
* 🍕 Assign individual food items to specific friends
* 💰 Calculate exactly how much each person owes
* 🧮 Handle taxes and other bill charges
* 📊 Display a clear final payment summary
* 🌐 Simple and interactive Streamlit interface

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Google Gemini API**
* **Pillow (PIL)**
* **Git & GitHub**

## 📂 Project Structure

```text
FairSplit_AI/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/FairSplit_AI.git
```

### 2. Open the project folder

```bash
cd FairSplit_AI
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Gemini API Key Setup

Create a `.streamlit` folder in the project directory if it does not already exist.

Inside it, create:

```text
secrets.toml
```

Add your Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

**Do not upload your API key to GitHub.**

Make sure `.gitignore` contains:

```text
.streamlit/secrets.toml
```

## ▶️ Run the Application

Run the following command in the project terminal:

```bash
py -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 📖 How It Works

1. Upload a bill image.
2. FairSplit AI analyzes the bill using Gemini AI.
3. The application extracts the food items and prices.
4. Add the people who shared the bill.
5. Assign each food item to the person who consumed it.
6. The application calculates each person's share.
7. View the final amount owed by each person.

## 💡 Example

Suppose a bill contains:

| Item   | Price | Person |
| ------ | ----: | ------ |
| Pizza  |  ₹400 | Sonali |
| Burger |  ₹200 | Rahul  |
| Pasta  |  ₹300 | Priya  |

FairSplit AI assigns the items individually and calculates the amount each person needs to pay.

## 🎯 Project Goal

The goal of FairSplit AI is to make splitting restaurant bills **simple, accurate, and fair** by calculating expenses based on the actual food items consumed by each person instead of simply dividing the total bill equally.

## 🔮 Future Improvements

* Automatic detection of who consumed each item
* Better handling of complex restaurant bills
* Support for multiple currencies
* Bill history and saved splits
* QR-code based payment integration
* Improved AI accuracy for low-quality bill images

## 👩‍💻 Author

**Sonali Agnihotri**

B.Tech Information Technology
Medicaps University, Indore

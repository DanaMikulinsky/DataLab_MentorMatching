# DataLab Final Project - MentorMatching  
🚀 AI-Driven Mentorship Platform for LinkedIn – Recommending optimal mentor-mentee matches using AI, LinkedIn profile data, and expertise grading. 🚀
---

## 📜 Acknowledgments  
This project was developed by **Anya Sukachev**, **Alexa Birenbaum**, **Liat Tsipory**, and **Dana Mikulinsky** as the **final project** for the **Data Lab course - 00940290**.  

🚀 Submitted in **February, 2025** (Winter semester)  

---

## 📑 Table of Contents  
- [📢 Important Notice](#-important-notice)  
- [📌 Part 1 - Web Scraping](#-part-1---web-scraping)  
  - [🌎 Shanghai Ranking Scraper](#-shanghai-ranking-scraper)  
  - [📚 Best Courses Scraper](#-best-courses-scraper)  
  - [🚀 How to Run the Scrapers Locally](#-how-to-run-the-scrapers-locally)  
  - [🛠️ Optional: Remove Duplicates](#-optional-remove-duplicates)  
- [📌 Part 2 - Data Preprocessing](#-part-2---data-preprocessing)  
- [📌 Part 3 - Execution & Evaluation](#-part-3---execution--evaluation)  
- [📌 Part 4 - Visualizations](#-part-4---visualizations)  
- [🔹 General Notes](#-general-notes)  


---

## 📢 Important Notice  
Parts **2-4** of this project can **only be run in Databricks** due to:  
✅ **PySpark Dependency** – The execution relies on **PySpark**, optimized for Databricks.  
✅ **Big Data Storage** – The dataset is **too large** to be exported and is stored in **Databricks DBFS**.  

**Part 1 (Scraping) is standalone and can be executed locally.**  

---
## 📌 Part 1 - Web Scraping  
<details>
<summary> This section contains two web scrapers designed to collect **essential ranking data** for mentor-mentee matching.  </summary>

<details>
  <summary>🌎 Shanghai Ranking Scraper (Click to expand)</summary>

Scrapes university ranking data from **[Shanghai Ranking](https://www.shanghairanking.com/)**, including:  
- **Academic Ranking of World Universities (ARWU) – 2024**  
- **Global Ranking of Sport Science Schools and Departments – 2024**  
- **Global Ranking of Academic Subjects (GRAS) – 2024**  

This data is used to **score the education level** of users based on the institution they attended.  
</details>  

<details>
  <summary>📚 Best Courses Scraper (Click to expand)</summary>

Collects a ranked list of top courses from **[Class Central](https://www.classcentral.com/collection/top-free-online-courses)**, providing insight into popular courses.  
- Helps assess **educational background** beyond traditional degrees.  

Both scrapers were built using **Selenium** and can be executed independently on any system with Python installed.  
</details>  
---

## 🚀 How to Run the Scrapers Locally  

### 1️⃣ Clone the Repository  
First, clone this repository to your local machine using:  

```sh
git clone https://github.com/your-username/DataLab_MentorMatching.git
cd DataLab_MentorMatching/part\ 1\ -\ scraping
```

### 2️⃣ Install Dependencies  
Ensure you have Python **3.8+** installed, then install the required dependencies:  

```sh
pip install -r requirements.txt
```

### 3️⃣ Run the Scrapers  

<details>
  <summary>📊 Shanghai Rankings Scraper</summary>

To scrape **Academic Rankings**, run:  

```sh
python scrape_shanghai.py
```

This will generate:  
- `academic_ranking_world_universities.csv` (ARWU 2024 university rankings)  
- `sport_science_ranking.csv` (Global ranking of sport science schools, if enabled in the script)  
</details>  

<details>
  <summary>📌 Categorized Shanghai Rankings Scraper (GRAS 2024)</summary>

To scrape **Global Ranking of Academic Subjects (GRAS) 2024**, run:  

```sh
python scrape_categories.py
```

This will generate:  
- `categorized_rankings.csv` (Category-based university rankings)  
</details>  

<details>
  <summary>📚 Best Courses Scraper (Class Central)</summary>

To scrape **top free online courses**, run:  

```sh
python scrape_courses.py
```

This will generate:  
- `top_courses.csv` (A list of the best free courses)  
</details>  

---

## 🛠️ Optional: Remove Duplicates  
If necessary, you can remove duplicates from the academic rankings dataset by running:  

```sh
python dups.py
```

---

## 🔹 Notes  
- **Shanghai Rankings** scraping relies on **Selenium**, so you must have **ChromeDriver** installed. The script automatically installs it via `webdriver-manager`.  
- **Class Central Scraper** uses Selenium and requires Chrome. It will load all courses dynamically by interacting with the "Load More" button.  
- Output files will be saved in the same directory as the script.  
</details>

---

## 📌 Part 2 - Data Preprocessing  
<details>
<summary>This stage processes LinkedIn user data, prepares features, and assigns expertise labels.  </summary>

### **How to Run**  
1️⃣ Upload the notebooks into a **Databricks Workspace**.  
2️⃣ Ensure access to **DBFS storage** for reading the datasets.  
3️⃣ Open and run each notebook in the specified order.  

### **Notebooks**  

- **`create users features.ipynb`** → Extracts and preprocesses user profile features from LinkedIn datasets.  
- **`expertise-level label assigning.ipynb`** → Assigns expertise scores to users based on education, work experience, and ranking data.  
- **`meta-industries labels assigning.ipynb`** → Categorizes users into broader industry groups using predefined meta-industry labels.  
</details>

---

## 📌 Part 3 - Execution & Evaluation  
<details>
<summary>This stage runs the **mentorship matching algorithm**, identifying the best mentors for mentees using a **K-Nearest Neighbors (KNN) approach**.  </summary>

### **How to Run**  
1️⃣ Upload the notebooks into a **Databricks Workspace**.  
2️⃣ Ensure all preprocessing steps from **Part 2** are completed.  
3️⃣ Open and execute the notebooks in the specified order.  

### **Notebooks**  

- **`Find mentors (KNN).ipynb`** → Implements the **K-Nearest Neighbors (KNN) algorithm** to find the most suitable mentors for a given user.  
- **`Mentors Matching Demo.ipynb`** → Demonstrates the mentorship matching process with sample queries and results.  
</details>

---

## 📌 Part 4 - Visualizations  
<details>
<summary>This section provides **data insights and visual representations** of the mentorship platform’s performance and user distribution.  </summary>

### **How to Run**  
1️⃣ Upload the notebook into a **Databricks Workspace**.  
2️⃣ Ensure that previous execution results are available.  
3️⃣ Run the notebook to generate visualizations.  

### **Notebook**  

- **`Visualizations.ipynb`** → Generates plots, charts, and insights to evaluate the effectiveness of the mentorship recommendations.  
</details>

---

### 🔹 **General Notes**  
- All notebooks should be run in **Databricks with access to DBFS**.  
- Ensure that **previous steps are completed** before running execution and visualization notebooks.  
- The **mentorship matching algorithm requires preprocessed data** from Part 2 before running.  

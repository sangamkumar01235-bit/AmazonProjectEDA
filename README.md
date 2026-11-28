# 🛒 Amazon India Product Catalog Analysis

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas)
![Status](https://img.shields.io/badge/Project-Completed-success)
![Dataset](https://img.shields.io/badge/Dataset-Amazon_India-orange?logo=amazon)

## 📌 Project Overview

This project focuses on analyzing the Amazon India Product Catalog dataset to understand product pricing, discounts, customer ratings, review volumes, and category distribution.

The project uses Exploratory Data Analysis (EDA) to identify patterns and insights in Amazon India's product listings.

## 📊 Dataset Information

The dataset (`amazon_cleaned.csv`) contains:

| Description | Details |
|---|---:|
| Total Records | 1,465 |
| Total Attributes | 20 |
| Unique Products | 1,351 |
| Main Categories | 9 |
| Subcategories | 29 |
| Category Leaf Nodes | 207 |
| Missing Values | 3 |
| Data Completeness | 99.99% |
| Currency | Indian Rupees (₹) |

## 🗂️ Dataset Attributes

The dataset contains the following attribute groups:

### 1. Product Identifiers
- `product_id`
- `img_link`
- `product_link`

### 2. Category Information
- `main_category`
- `subcategory`
- `category_leaf`
- `category_path`

### 3. Pricing and Discounts
- `discounted_price`
- `actual_price`
- `discount_amount`
- `discount_percentage`

### 4. Customer Reviews
- `rating`
- `rating_count`
- `user_id`
- `user_name`
- `review_id`
- `review_title`
- `review_content`

### 5. Product Information
- `product_name`
- `about_product`

## 📈 Statistical Analysis

| Metric | Mean | Median |
|---|---:|---:|
| Discounted Price | ₹3,125.31 | ₹799 |
| Actual Price | ₹5,444.99 | ₹1,650 |
| Discount Amount | ₹2,319.68 | ₹800 |
| Discount Percentage | 47.69% | 50% |
| Product Rating | 4.10 | 4.10 |
| Rating Count | 18,296 | 5,179 |

### 💰 Pricing Insights
- Average discounted product price is ₹3,125.31.
- Average actual price is ₹5,444.99.
- Average discount percentage is 47.69%.
- Half of the products have discounts of 50% or higher.
- Product prices show a strong positive skew.

## 📦 Category-Wise Analysis

| Category | Listings | Share | Average Price | Average Discount | Average Rating |
|---|---:|---:|---:|---:|---:|
| Electronics | 526 | 35.9% | ₹5,965.89 | 50.8% | 4.08 |
| Computers & Accessories | 453 | 30.9% | ₹842.65 | 54.0% | 4.15 |
| Home & Kitchen | 448 | 30.6% | ₹2,330.62 | 40.1% | 4.04 |
| Office Products | 31 | 2.1% | ₹301.58 | 12.4% | 4.31 |
| Other Categories | 7 | 0.5% | ₹823 | 42.1% | 4.06 |

## 🔍 Key Findings

1. **Category Distribution:** Electronics has the highest number of listings, accounting for 35.9% of the dataset.

2. **Discount Analysis:** Computers & Accessories offers the highest average discount of 54%.

3. **Customer Ratings:** Average product rating is 4.10 out of 5.

4. **Popular Product Categories:** USB Cables is the largest leaf category with 233 listings.

5. **Review Analysis:** Amazon Basics High-Speed HDMI Cables have 426,973 ratings, followed by boAt Bassheads 100 Earphones with 363,713 ratings.

6. **Category Concentration:** Electronics, Computers & Accessories, and Home & Kitchen together account for 97.4% of all listings.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## ⚙️ Installation and Usage

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
```

### Step 2: Navigate to the project directory

```bash
cd your-repository
```

### Step 3: Install required libraries

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### Step 4: Load the dataset

```python
import pandas as pd

df = pd.read_csv("amazon_cleaned.csv")

print(df.head())
print(df.info())
print(df.describe())
```

## 📁 Project Structure

```text
Amazon-India-Analysis/
│
├── amazon_cleaned.csv
├── AmazonEDAProject.ipynb
├── README.md
└── requirements.txt
```

## 🎯 Project Objectives

- Analyze Amazon India product listings.
- Understand product pricing patterns.
- Examine discount percentages.
- Identify popular product categories.
- Analyze customer ratings and reviews.
- Discover useful business insights through data analysis.

## 👨‍💻 Author

**Sangam Kumar**

Data Analytics | Python | SQL | Data Visualization

---

⭐ If you find this project interesting, consider giving this repository a star!

**Project:** Amazon India Product Catalog Analysis  
**Dataset:** Amazon India Product Catalog (`amazon_cleaned.csv`)

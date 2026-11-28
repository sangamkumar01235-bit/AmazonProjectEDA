# 🛒 Amazon India Product Sales & Pricing Analysis

An exploratory data analysis (EDA) and visualization project examining **1,465 product listings** (`1,351` unique products) from Amazon India. This repository explores product pricing strategies, discount distributions, customer ratings, and category-level market trends.

---

## 📊 Dataset Overview

The dataset (`amazon_cleaned.csv`) contains **1,465 records** across **20 features**, capturing pricing, discount structures, hierarchical categories, and aggregated customer reviews.

* **Total Records:** 1,465 rows × 20 columns
* **Unique Products:** 1,351 (`product_id`)
* **Data Completeness:** 99.99% complete (only 1 missing value in `rating` and 2 in `rating_count`)
* **Currency:** Indian Rupees (₹)

### 🗂️ Schema Summary

| Feature Group | Columns | Description |
| :--- | :--- | :--- |
| **Identifiers & Links** | `product_id`, `img_link`, `product_link` | Unique product IDs and direct URLs to product pages/images |
| **Categorization** | `main_category`, `subcategory`, `category_leaf`, `category_path` | Multi-level product taxonomy (9 main categories, 207 leaf categories) |
| **Pricing & Discounts** | `discounted_price`, `actual_price`, `discount_amount`, `discount_percentage` | Original MRP, selling price, absolute savings, and discount percentage |
| **Ratings & Reviews** | `rating`, `rating_count`, `user_id`, `user_name`, `review_id`, `review_title`, `review_content` | Star ratings (1–5), total review counts, and top customer review text |
| **Product Metadata** | `product_name`, `about_product` | Product titles and detailed feature descriptions |

---

## 📈 Key Statistical Highlights

| Metric | Mean | Median | Min | Max |
| :--- | :---: | :---: | :---: | :---: |
| **Discounted Price (₹)** | ₹3,125.31 | ₹799.00 | ₹39.00 | ₹77,990.00 |
| **Actual Price (₹)** | ₹5,444.99 | ₹1,650.00 | ₹39.00 | ₹139,900.00 |
| **Discount Percentage** | 47.69% | 50.00% | 0% | 94% |
| **Product Rating (1–5)** | 4.10 | 4.10 | 2.00 | 5.00 |
| **Rating Count** | 18,296 | 5,179 | 2 | 426,973 |

### 🔍 Core Insights
* **Category Dominance:** Three primary categories—**Electronics** (35.9%), **Computers & Accessories** (30.9%), and **Home & Kitchen** (30.6%)—make up **97.4%** of all listings.
* **Right-Skewed Pricing:** Half of the catalog is priced at **₹799 or below**, while high-ticket appliances (such as Smart TVs up to ₹77,990) pull the average price up.
* **Aggressive Discounting:** The median discount across the dataset is **50%**, with discounts reaching up to **94%** off on select accessories.
* **High Customer Satisfaction:** Ratings are tightly clustered between **4.0 and 4.3 stars** across major categories.

---

## 📉 Visual Charts & Exploratory Analysis

To uncover deeper trends and distributions within the dataset, the following **5 visual charts** were created and included in this project:

1. **🥧 Pie Chart — Category Market Share**
   * Illustrates the proportional share of listings across main product categories, highlighting the dominance of Electronics, Computers & Accessories, and Home & Kitchen.
2. **📊 Bar Chart — Top Subcategories & Average Pricing**
   * Compares listing volumes, average discounted prices, and customer review engagement across top-performing subcategories (e.g., *USB Cables*, *Smart Watches*, *Smartphones*).
3. **📶 Histogram — Discount Percentage & Rating Distributions**
   * Displays the frequency distribution of product discounts (peaking around 50%–60%) and customer star ratings (heavily concentrated between 4.0 and 4.4).
4. **🔵 Scatter Plot — Price vs. Rating & Discount Relationships**
   * Examines correlations between `actual_price`, `discounted_price`, `discount_percentage`, and customer `rating` to identify whether higher discounts drive better ratings or higher review volume.
5. **📦 Box Plot — Price Spread & Outlier Detection by Category**
   * Visualizes median prices, interquartile ranges (IQR), and high-value outliers across major categories to highlight pricing dispersion.

---

## 🚀 How to Use
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/amazon-india-eda.git
   ```
2. Open the dataset (`amazon_cleaned.csv`) and analysis notebook/script to explore the code behind the charts.
3. View the rendered charts in the `visualizations/` folder (or notebook outputs).
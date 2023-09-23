# E7 Hero Data Project Documentation

## Table of Contents

1. [Introduction](#introduction)
   - [Project Overview](#project-overview)
   - [Key Features](#key-features)
   - [Dependencies](#dependencies)

2. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Setup](#setup)

3. [Usage](#usage)
   - [1. Data Scraping (e7xscrape.py)](#1-data-scraping-e7xscrapepy)
   - [2. Data Visualization (e7visualization.py)](#2-data-visualization-e7visualizationpy)
   - [3. Supplementary Analysis (e7supplementary.py)](#3-supplementary-analysis-e7supplementarypy)
   - [4. Interactive Dashboard (e7dash.py)](#4-interactive-dashboard-e7dashpy)

4. [Project Structure](#project-structure)

5. [Contributing](#contributing)

6. [License](#license)

## 1. Introduction <a name="introduction"></a>

### Project Overview <a name="project-overview"></a>

The "E7 Hero Data" project is a Python-based initiative aimed at collecting, analyzing, and visualizing character data from the popular mobile game "Epic Seven." This documentation provides an in-depth overview of the project, its features, and how to use it effectively.

### Key Features <a name="key-features"></a>

- **Data Scraping (e7xscrape.py):** Web scraping script to collect character data from the Epic Seven website.

- **Data Visualization (e7visualization.py):** Generates percentile-based line plots to visualize character statistics across different categories.

- **Supplementary Analysis (e7supplementary.py):** Produces bar plots displaying average statistics based on character attributes like rarity, class, and horoscope.

- **Interactive Dashboard (e7dash.py):** A web application that allows users to explore character data interactively, including image display and comments.

### Dependencies <a name="dependencies"></a>

The project relies on several Python libraries and modules, including:

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/): For web scraping and parsing HTML content.
- [Pandas](https://pandas.pydata.org/): For data manipulation and storage.
- [Matplotlib](https://matplotlib.org/): For data visualization.
- [Seaborn](https://seaborn.pydata.org/): For creating statistical graphics.
- [Dash](https://dash.plotly.com/): For building the interactive dashboard.

## 2. Installation <a name="installation"></a>

### Prerequisites <a name="prerequisites"></a>

Ensure that you have the following prerequisites installed on your system:

- Python 3.x
- Pip (Python package manager)

### Setup <a name="setup"></a>

1. Clone the project repository:
   ```bash
   git clone https://github.com/yourusername/e7hero-data.git
   ```

2. Navigate to the project directory:
   ```bash
   cd e7hero-data
   ```

3. Install project dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## 3. Usage <a name="usage"></a>

### 1. Data Scraping (e7xscrape.py) <a name="1-data-scraping-e7xscrapepy"></a>

- This script extracts character data from the Epic Seven website and stores it in a CSV file named "e7HeroData.csv."

- To run the script, execute the following command:
  ```bash
  python e7xscrape.py
  ```

### 2. Data Visualization (e7visualization.py) <a name="2-data-visualization-e7visualizationpy"></a>

- This script generates percentile-based line plots to visualize character statistics for different categories.

- To run the script, execute the following command:
  ```bash
  python e7visualization.py
  ```

### 3. Supplementary Analysis (e7supplementary.py) <a name="3-supplementary-analysis-e7supplementarypy"></a>

- This script creates bar plots to display average statistics based on character attributes like rarity, class, and horoscope.

- To run the script, execute the following command:
  ```bash
  python e7supplementary.py
  ```

### 4. Interactive Dashboard (e7dash.py) <a name="4-interactive-dashboard-e7dashpy"></a>

- The interactive dashboard allows users to explore character data, view character images, and read comments.

- To launch the dashboard, run the following command:
  ```bash
  python e7dash.py
  ```

## 4. Project Structure <a name="project-structure"></a>

The project directory is organized as follows:

- `e7xscrape.py`: Web scraping script for data collection.
- `e7visualization.py`: Script for generating percentile-based line plots.
- `e7supplementary.py`: Script for supplementary data analysis.
- `e7dash.py`: Dash web application for the interactive dashboard.
- `assets/`: Directory containing assets such as images and CSS.
- `plots/`: Directory for storing generated plots.
- `comments/`: Directory for comments associated with the generated plots.
- `e7HeroData.csv`: CSV file containing character data.
- `requirements.txt`: List of project dependencies.

## 5. Contributing <a name="contributing"></a>

Contributions to this project are welcome. Please follow the standard GitHub fork and pull request workflow. Be sure to adhere to the project's coding and documentation standards.

## 6. License <a name="license"></a>

This project is licensed under the [MIT License](LICENSE).

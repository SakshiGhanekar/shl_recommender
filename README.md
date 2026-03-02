# SHL Assessment Recommender System

An intelligent recommendation system that simplifies the process of finding the right SHL assessments for various job roles.

## Features

- **389 assessments** crawled from the SHL product catalog.
- **Intelligent matching** using BM25 and keyword-boosted lexical search.
- **Premium Web Interface** with a modern dark-themed, glassmorphism design.
- **REST API** endpoint for programmatically fetching recommendations.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd shl-recommender
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the assessment data is present:
   - `assessments_full.json` (Included in the repo)

## Usage

### Starting the Server

Run the Flask application:

```bash
python main.py
```

The application will be available at `http://localhost:5000`.

### API Documentation

**Endpoint:** `POST /predict`
**Payload:**

```json
{
  "query": "Looking for senior Java engineers with cloud experience..."
}
```

**Response:**
Returns a JSON list of 5-10 recommended assessments with their names, URLs, and match scores.

## Data Crawling

The assessment data was gathered using a two-stage crawling process:

1. `crawl_urls.py`: Extracts URLs and names for all "Individual Test Solutions" from the SHL catalog.
2. `crawl_details.py`: Fetches detailed descriptions and metadata for each assessment to improve matching accuracy.

## Project Structure

- `main.py`: Flask application server.
- `recommender.py`: Core recommendation engine logic.
- `index.html`: Modern frontend interface.
- `generate_predictions.py`: Script to generate predictions for the test set.
- `predictions.csv`: Generated predictions for the provided test dataset.
- `Gen_AI Dataset.xlsx`: Original dataset for training and testing.

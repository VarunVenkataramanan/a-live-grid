# LiveGrid-Om Setup Guide

## Environment Setup

1. **Google Cloud Setup**
   - Create a GCP project and enable Pub/Sub API.
   - Create a Pub/Sub topic (e.g., `city-events`) and a subscription (e.g., `event-processor`).
   - Create a service account with Pub/Sub Publisher and Subscriber roles.
   - Download the service account JSON key and set the environment variable:
     - Linux/macOS: `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp-key.json"`
     - Windows PowerShell: `$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\gcp-key.json"`
   - Set additional environment variables as needed:
     - `GCP_PROJECT_ID`, `PUBSUB_TOPIC_ID`, `PUBSUB_SUBSCRIPTION_ID`

2. **Google Custom Search API**
   - Create a Programmable Search Engine and get the Search Engine ID.
   - Enable the Custom Search API and get an API key.
   - Set environment variables:
     - `GOOGLE_CSE_API_KEY`, `GOOGLE_CSE_ID`

3. **Local Development**
   - Install dependencies: `pip install -r requirements.txt` in each module as needed.
   - To use the Pub/Sub emulator for local testing, see: https://cloud.google.com/pubsub/docs/emulator

4. **Running the Pipeline**
   - Ingestor: Fetches data, filters by keywords, and publishes to Pub/Sub.
   - Extraction Worker: Subscribes to Pub/Sub, processes messages through LLM, and extracts structured civic signals.
   - Google CSE Source: Fetches web results and publishes to Pub/Sub.
   - LLM Processing: Uses Ollama (gemma:7b) to extract structured data from text.

5. **Cleanup**
   - Delete unused GCP resources after the hackathon to avoid charges.

## Architecture

The system now focuses on LLM processing:
- **Data Ingestion**: Multiple sources (Twitter, Reddit, News, Google CSE)
- **Pub/Sub**: Real-time message streaming
- **LLM Processing**: Structured extraction of civic signals
- **JSON Output**: Ready for feeding to your main LLM application

## Testing

Run the test scripts to verify your setup:
- `python test_google_cse.py` - Test Google CSE integration
- `python test_full_pipeline.py` - Test the complete pipeline 
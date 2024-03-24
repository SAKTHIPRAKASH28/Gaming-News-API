# FastAPI Gaming News Aggregator

This FastAPI application aggregates gaming news from multiple sources and allows users to retrieve news based on specific topics.

## Features

- Fetches gaming news from GameRant and PC Gamer websites.
- Allows filtering news by topics.
- Implements caching mechanism to improve performance.
- Asynchronous fetching of news articles.

## Dependencies

- Python 3.7+
- FastAPI
- uvicorn
- BeautifulSoup
- httpx
- cachetools

## Setup

1. Clone the repository:

2. Install dependencies:

## Usage

1. Run the application:

2. Access the API using a web browser or tools like cURL or Postman:

- To get all news articles:
  - [http://localhost:8080/](http://localhost:8080/)
- To filter news articles by topic:
  - [http://localhost:8080/?topic=your_topic](http://localhost:8080/?topic=your_topic)

Replace `your_topic` with the desired topic for filtering news articles.

## Hosted Link

You can access the hosted version of this application at [your_hosted_link](your_hosted_link).

## API Endpoints

- `GET /`: Retrieve all news articles or filter by topic.
  - Query Parameter:
    - `topic`: Optional. Filter news articles by topic.

## Caching

The application implements caching using the `TTLCache` from `cachetools` to store previously fetched news articles for faster retrieval.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

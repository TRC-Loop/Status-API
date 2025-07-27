# Status-API

A FastAPI-based system metrics API that provides detailed information about CPU, RAM, Disk, Network, OS, and system uptime. The API requires an API key for access, which is configured via environment variables.

## Features

- Retrieve system uptime
- CPU information and usage percentages
- Memory (RAM) usage
- Disk partitions and usage
- Operating system details
- Network interfaces and statistics
- Default shell information

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt` (or install via pip)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/TRC-Loop/Status-API.git
cd Status-API
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

```bash
pip install fastapi uvicorn psutil cpuinfo
```

## Configuration

Set the environment variable `API_KEY_STATS` to your secret key:

```bash
export API_KEY_STATUS="your-secret-api-key"
```

On Windows Command Prompt:

```cmd
set API_KEY_STATUS=your-secret-api-key
```

## Running the Server

Start the server with Uvicorn:

```bash
uvicorn main:app --reload
```
*If in src/ dir, otherwise use `src.main:app`*

Replace `main:app` with the correct module path if your file is located elsewhere.

## Accessing the API

- Base URL: `http://localhost:8000`

### Authentication

Include the API key in the request headers:

```
X-API-KEY: your-secret-api-key
```

### Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Environment Variables

- `API_KEY_STATUS`: Your secret API key for authentication.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Notes

- Ensure your environment variable `API_KEY_STATUS` is set before running the server.
- The API is designed for open-source use; keep your API key secure and do not expose it publicly.

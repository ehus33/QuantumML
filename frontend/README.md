# Quantum Healthcare Optimizer UI

A modern React TypeScript web interface for the quantum healthcare optimization system.

## Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

3. Make sure the API server is running on port 5000:
```bash
# In the root directory
python app.py
```

## Features

- **Configuration Panel**: Adjust experiment parameters in real-time
- **Results Visualization**: Compare quantum vs classical optimization methods
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **Responsive Design**: Works on desktop and mobile devices

## API Integration

The UI connects to the Flask API at `http://localhost:5000` by default. You can override this by setting the `REACT_APP_API_URL` environment variable.

```bash
REACT_APP_API_URL=http://localhost:5000 npm start
```

## Technology Stack

- React 18 with TypeScript
- Tailwind CSS for styling
- Lucide React for icons
- Axios for API communication
- Create React App for development

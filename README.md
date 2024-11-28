# Akira - Mind Map Generator

Akira is an innovative web application that transforms your markdown notes into interactive mind maps. By leveraging natural language processing and graph visualization using TF-IDF scores and Jaccard-Similarity, Akira helps you understand and connect ideas across multiple documents.

## Features

- 🔄 Drag-and-drop file upload
- 📝 Markdown file processing
- 🗺️ Interactive mind map visualization
- 🔍 Zoomable and pannable graphs
- 🔗 Automatic topic connection detection

## Tech Stack

### Frontend

- React + Vite
- TailwindCSS for styling
- Mermaid.js for mind map visualization
- Lucide React for icons

### Backend

- Flask (Python)
- NLTK for natural language processing
- scikit-learn for topic extraction
- Beautiful Soup for text processing

### Prerequisites

- [devenv | nix ](https://devenv.sh/)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/akira.git
cd akira
```

2. Initialise development environment:

```bash
devenv up
```

3. Install frontend dependencies:

```bash
cd akira-frontend
npm install
```

4. Download required NLTK data:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### Running the Application

1. In the root directory

```bash
devenv up
```

## Usage

1. Navigate to the upload page
2. Drag and drop your markdown files or click to select them
3. Click "Process Files" to generate the mind map
4. Use the zoom controls and drag to explore the generated mind map
5. View extracted topics and connections below the visualization

## Features in Detail

### File Upload

- Supports markdown (.md) files
- Multiple file upload
- Progress indication
- Error handling

### Mind Map Visualization

- Interactive graph with zoom and pan controls
- Topic clustering by file
- Automatic connection detection between related topics
- Dark theme optimized for readability

### Topic Extraction

- AI-powered topic identification
- Relevance scoring
- Cross-document topic linking
- Natural language processing

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a pull request

## License

This project is licensed under the GPL3 License - see the LICENSE file for details.

## Acknowledgments

- Built with React and Flask
- Uses NLTK for natural language processing
- Visualization powered by Mermaid.js
- Styled with TailwindCSS

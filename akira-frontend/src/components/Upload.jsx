import { useState, useEffect } from "react";
import FileUpload from "./FileUpload";
import AkiraLogo from "../assets/vite.svg";
import { Link } from "react-router-dom";
import { Loader } from "lucide-react";
import mermaid from "mermaid";
import MermaidGraph from "./Mermaid";

// const MermaidGraph = ({ diagram }) => {
//   const [svg, setSvg] = useState("");
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const renderDiagram = async () => {
//       try {
//         // Decode the base64 encoded diagram
//         const decodedDiagram = atob(diagram);
//         console.log("Decoded diagram:", decodedDiagram); // For debugging

//         // Configure mermaid
//         mermaid.initialize({
//           startOnLoad: true,
//           theme: "dark",
//           securityLevel: "loose",
//           mindmap: {
//             padding: 100,
//             useMaxWidth: true,
//           },
//         });

//         // Generate SVG
//         const { svg } = await mermaid.render("mermaid-graph", decodedDiagram);
//         setSvg(svg);
//         setError(null);
//       } catch (error) {
//         console.error("Failed to render diagram:", error);
//         setError(error.message);
//       }
//     };

//     if (diagram) {
//       renderDiagram();
//     }
//   }, [diagram]);

//   if (error) {
//     return (
//       <div className="mt-8 p-6 bg-red-500/20 border border-red-500 rounded-lg text-red-200">
//         Failed to render diagram: {error}
//       </div>
//     );
//   }

//   return (
//     <div className="mt-8 p-6 bg-gray-800 rounded-lg overflow-auto">
//       {svg ? (
//         <div
//           dangerouslySetInnerHTML={{ __html: svg }}
//           className="min-w-full"
//           style={{ minWidth: "800px" }}
//         />
//       ) : (
//         <div className="text-gray-400">Loading diagram...</div>
//       )}
//     </div>
//   );
// };

const LoadingSpinner = () => (
  <div className="flex items-center justify-center mt-8">
    <Loader className="w-8 h-8 text-purple-500 animate-spin" />
    <span className="ml-2 text-lg text-gray-300">Generating mind map...</span>
  </div>
);

export default function Upload() {
  const [files, setFiles] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [graphData, setGraphData] = useState(null);
  const [error, setError] = useState(null);

  const processFiles = async () => {
    const formData = new FormData();
    files.forEach((file, index) => {
      formData.append(`file${index}`, file);
    });

    setIsProcessing(true);
    setGraphData(null);
    setError(null);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed with status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Response:", data);

      if (data.analysis && data.analysis.diagram) {
        setGraphData(data.analysis);
      } else {
        throw new Error("No diagram data received");
      }

      setFiles([]); // Clear files after successful upload
    } catch (error) {
      console.error("Upload failed:", error);
      setError(error.message);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <nav className="px-6 py-4">
        <Link to="/">
          <div className="flex items-center space-x-2">
            <img src={AkiraLogo} alt="Logo" className="w-24 h-24" />
            <span className="text-4xl font-semibold">Akira</span>
          </div>
        </Link>
      </nav>
      <main className="container mx-auto px-6 pt-20 pb-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Upload Your Documents
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl">
            Easily upload your files and get a graph mind mapped to boost
            productivity.
          </p>
          <FileUpload files={files} setFiles={setFiles} />

          {error && (
            <div className="mt-4 p-4 bg-red-500/20 border border-red-500 rounded-lg text-red-200">
              {error}
            </div>
          )}

          {files.length > 0 && (
            <button
              onClick={processFiles}
              disabled={isProcessing}
              className={`mt-4 w-full py-3 rounded-lg font-medium transition-colors ${
                isProcessing
                  ? "bg-purple-400 cursor-not-allowed"
                  : "bg-purple-600 hover:bg-purple-700"
              }`}
            >
              {isProcessing ? "Processing..." : "Process Files"}
            </button>
          )}

          {isProcessing && <LoadingSpinner />}

          {graphData && !isProcessing && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold mb-4">Generated Mind Map</h2>
              <MermaidGraph diagram={graphData.diagram} />

              {/* File topics display */}
              <div className="mt-8">
                <h3 className="text-xl font-bold mb-4">File Topics</h3>
                <div className="grid gap-4 md:grid-cols-2">
                  {Object.entries(graphData.file_topics).map(
                    ([filename, data]) => (
                      <div
                        key={filename}
                        className="bg-gray-800/50 p-4 rounded-lg"
                      >
                        <h4 className="font-semibold mb-2">{filename}</h4>
                        <div className="text-sm text-gray-300">
                          <div className="mb-2">
                            <strong>Topics:</strong>
                            <div className="flex flex-wrap gap-2 mt-1">
                              {data.topics.map((topic, i) => (
                                <span
                                  key={i}
                                  className="px-2 py-1 bg-purple-500/20 rounded-full text-xs"
                                >
                                  {topic}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    ),
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

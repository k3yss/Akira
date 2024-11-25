import { useState } from "react";
import FileUpload from "./FileUpload";
import AkiraLogo from "../assets/vite.svg";
import { Link } from "react-router-dom";

export default function Upload() {
  const [files, setFiles] = useState([]);

  const processFiles = async () => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("file", file);
    });
    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      console.log(data.message);
      setFiles([]); // Clear files after successful upload
    } catch (error) {
      console.error("Upload failed:", error);
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
          {files.length > 0 && (
            <button
              onClick={processFiles}
              className="mt-4 w-full py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-medium"
            >
              Process Files
            </button>
          )}
        </div>
      </main>
    </div>
  );
}

import FileUpload from "./FileUpload";
import AkiraLogo from "../assets/vite.svg";
import { Link } from "react-router-dom";

export default function Upload() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      {/* Navigation */}
      <nav className="px-6 py-4">
        <Link to="/">
          <div className="flex items-center space-x-2">
            <img src={AkiraLogo} alt="Logo" className="w-24 h-24" />
            <span className="text-4xl font-semibold">Akira</span>
          </div>
        </Link>
      </nav>

      {/* Upload Section */}
      <main className="container mx-auto px-6 pt-20 pb-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Upload Your Documents
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl">
            Easily upload your files and get a graph mind mapped to boost
            productivity.
          </p>
          <FileUpload />
        </div>
      </main>
    </div>
  );
}

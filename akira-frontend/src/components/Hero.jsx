import React from "react";
import AkiraLogo from "../assets/vite.svg";
import { Link } from "react-router-dom";
import { Brain, GitGraph, Sparkles, ArrowRight } from "lucide-react";

const Hero = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      {/* Navigation */}
      <nav className="px-6 py-4">
        <div className="flex items-center space-x-2">
          <img src={AkiraLogo} alt="Vite Logo" className="w-24 h-24" />
          <span className="text-4xl font-semibold">Akira</span>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-6 pt-20 pb-16">
        <div className="max-w-4xl">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Hello, <span className="text-purple-400">thinker</span>
          </h1>

          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            The future of note taking
          </h2>

          <p className="text-xl text-gray-300 mb-8 max-w-2xl">
            Transform your markdown notes into beautiful mind maps. Connect
            ideas, visualize relationships, and boost your productivity by 10x
            with knowledge graphs.
          </p>

          {/* Email Signup */}
          <div className="flex flex-col sm:flex-row gap-4 max-w-xl mb-12">
            <Link to="/upload">
              <button className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-medium flex items-center justify-center group transition-colors">
                Get Started
                <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </Link>
          </div>

          {/* Feature Highlights */}
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-700">
              <GitGraph className="w-10 h-10 text-purple-400 mb-4" />
              <h3 className="text-xl font-semibold mb-2">Mind Mapped Graphs</h3>
              <p className="text-gray-400">
                Automatically generate beautiful knowledge graphs from your
                markdown notes
              </p>
            </div>

            <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-700">
              <Sparkles className="w-10 h-10 text-purple-400 mb-4" />
              <h3 className="text-xl font-semibold mb-2">Helpful Insights</h3>
              <p className="text-gray-400">
                Discover hidden connections and patterns in your notes
              </p>
            </div>

            <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-700">
              <Brain className="w-10 h-10 text-purple-400 mb-4" />
              <h3 className="text-xl font-semibold mb-2">Boost Productivity</h3>
              <p className="text-gray-400">
                Navigate your knowledge base efficiently and retain information
                better
              </p>
            </div>
          </div>
        </div>

        {/* Placeholder for Graph Visualization */}
      </main>
    </div>
  );
};

export default Hero;

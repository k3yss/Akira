import React, { useState, useEffect, useRef } from "react";
import mermaid from "mermaid";
import { ZoomIn, ZoomOut, MoveHorizontal } from "lucide-react";

const MermaidGraph = ({ diagram }) => {
  const [svg, setSvg] = useState("");
  const [error, setError] = useState(null);
  const [scale, setScale] = useState(1);
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [startPos, setStartPos] = useState({ x: 0, y: 0 });
  const containerRef = useRef(null);

  useEffect(() => {
    const renderDiagram = async () => {
      try {
        const decodedDiagram = atob(diagram);
        console.log(decodedDiagram);

        mermaid.initialize({
          startOnLoad: true,
          theme: "dark",
          //   securityLevel: "loose",
          //   mindmap: {
          //     padding: 1,
          //     useMaxWidth: false,
          //   },
          //   themeVariables: {
          //     // Updated colors for better dark theme integration
          //     mindmapBg: "#0f172a", // Darker background
          //     mindmapStroke: "#64748b", // Softer lines
          //     fontSize: "12px",
          //     mainBkg: "#1e293b", // Darker node background
          //     nodeBorder: "#334155", // Softer node borders
          //     nodeTextColor: "#e2e8f0", // Slightly softer text
          //     lineColor: "#475569", // More subtle connection lines

          //     // Additional color variables for better visual hierarchy
          //     primaryColor: "#3b82f6", // Blue accent for important nodes
          //     primaryTextColor: "#eff6ff",
          //     secondaryColor: "#0f172a",
          //     tertiaryColor: "#1e293b",
          //   },
        });

        const { svg } = await mermaid.render("mermaid-graph", decodedDiagram);
        setSvg(svg);
        setError(null);
      } catch (error) {
        console.error("Failed to render diagram:", error);
        setError(error.message);
      }
    };

    if (diagram) {
      renderDiagram();
    }
  }, [diagram]);

  // Rest of the component code remains the same
  const handleMouseDown = (e) => {
    if (e.button === 0) {
      setIsDragging(true);
      setStartPos({
        x: e.clientX - position.x,
        y: e.clientY - position.y,
      });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPosition({
        x: e.clientX - startPos.x,
        y: e.clientY - startPos.y,
      });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleZoom = (direction) => {
    setScale((prevScale) => {
      const newScale =
        direction === "in"
          ? Math.min(prevScale + 0.2, 3)
          : Math.max(prevScale - 0.2, 0.5);
      return newScale;
    });
  };

  const resetView = () => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
  };

  if (error) {
    return (
      <div className="mt-8 p-6 bg-red-500/20 border border-red-500 rounded-lg text-red-200">
        Failed to render diagram: {error}
      </div>
    );
  }

  return (
    <div className="mt-8">
      <div className="flex items-center gap-2 mb-4">
        <button
          onClick={() => handleZoom("in")}
          className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
          title="Zoom In"
        >
          <ZoomIn className="w-5 h-5" />
        </button>
        <button
          onClick={() => handleZoom("out")}
          className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
          title="Zoom Out"
        >
          <ZoomOut className="w-5 h-5" />
        </button>
        <button
          onClick={resetView}
          className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
          title="Reset View"
        >
          <MoveHorizontal className="w-5 h-5" />
        </button>
        <span className="text-sm text-gray-400">
          {Math.round(scale * 100)}%
        </span>
      </div>

      <div
        ref={containerRef}
        className="bg-gray-900 rounded-lg overflow-hidden"
        style={{
          height: "600px",
          cursor: isDragging ? "grabbing" : "grab",
        }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        {svg ? (
          <div
            dangerouslySetInnerHTML={{ __html: svg }}
            style={{
              transform: `scale(${scale}) translate(${position.x / scale}px, ${
                position.y / scale
              }px)`,
              transformOrigin: "0 0",
              transition: "transform 0.1s ease",
              minWidth: "1200px",
              padding: "20px",
            }}
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            Loading diagram...
          </div>
        )}
      </div>

      <div className="mt-4 text-sm text-gray-400">
        Tip: Click and drag to pan, use buttons above to zoom in/out
      </div>
    </div>
  );
};

export default MermaidGraph;

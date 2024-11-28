from collections import defaultdict


class TopicConnector:
    def __init__(self) -> None:
        self.file_topics = {}

    def add_file_topics(self, filename, topics, scores):
        """Store topics and scores for a file"""
        self.file_topics[filename] = {"topics": topics, "scores": scores}

    def find_connections(self, similarity_threshold=0.3):
        """Find connections between topics among files"""
        connections = defaultdict(list)
        files = list(self.file_topics.keys())

        if len(files) < 2:
            return connections

        for i, file1 in enumerate(files):
            for file2 in files[i + 1 :]:
                topics1 = self.file_topics[file1]["topics"]
                topics2 = self.file_topics[file2]["topics"]

                for topic1 in topics1:
                    terms1 = set(topic1.split("_"))
                    for topic2 in topics2:
                        terms2 = set(topic2.split("_"))

                        similarity = len(terms1 & terms2) / len(terms1 | terms2)

                        if similarity >= similarity_threshold:
                            connection = {
                                "files": (file1, file2),
                                "topics": (topic1, topic2),
                                "similarity": similarity,
                            }
                            connections[topic1].append(connection)
                            connections[topic2].append(connection)
        print(f"Connections: {connections}")
        return connections


class MermaidGenerator:
    def __init__(self) -> None:
        self.diagram = []

    def clean_topic(self, topic):
        """Cleanup topic name for mermaid compatibility"""
        return topic.replace(" ", "_").replace("-", "_")

    def create_mindmap(self, file_topics, connections):
        """
        Generate hierarchical mindmap with properly connected shared topics
        """
        diagram_parts = ["mindmap"]
        diagram_parts.append("  root((Topic Analysis))")

        # Track shared topics
        topic_occurrences = defaultdict(list)
        for filename, data in file_topics.items():
            for topic in data["topics"]:
                topic_occurrences[topic].append(filename)

        # Add file nodes first
        for filename in file_topics.keys():
            clean_filename = self.clean_topic(filename)
            diagram_parts.append(f"    {clean_filename}[{filename}]")

            # Add topics under each file
            file_data = file_topics[filename]
            for topic in file_data["topics"]:
                cleaned_topic = self.clean_topic(topic)
                # If topic appears in multiple files, add it with a unique identifier
                if len(topic_occurrences[topic]) > 1:
                    node_id = f"{cleaned_topic}_{clean_filename}"
                    diagram_parts.append(f"      {node_id}({topic})")
                else:
                    # For non-shared topics, add them directly
                    diagram_parts.append(f"      {cleaned_topic}({topic})")

        # Add connections for shared topics
        for topic, files in topic_occurrences.items():
            if len(files) > 1:
                cleaned_topic = self.clean_topic(topic)
                # Create connections between shared topic nodes
                file_nodes = [f"{cleaned_topic} - {self.clean_topic(f)}" for f in files]
                for i in range(len(file_nodes) - 1):
                    diagram_parts.append(f"    {file_nodes[i]} --- {file_nodes[i + 1]}")

        return "\n".join(diagram_parts)

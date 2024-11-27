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
            for file2 in files[i + 1]:
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
        return connections


class MermaidGenerator:
    def __init__(self) -> None:
        self.diagram = []

    def clean_topic(self, topic):
        """Cleanup topic name for mermaid compatibility"""
        return topic.replace(" ", "_").replace("-", "_")

    def create_mindmap(self, file_topics, connections):
        """
        Generate mindmap showing file topics and connections
        """
        diagram_parts = ["mindmap\n"]
        diagram_parts.append("root[Topic Analysis]\n")

        for filename, data in file_topics.items():
            clean_filename = self.clean_topic(filename)
            diagram_parts.append(f"{clean_filename}[File: {filename}]")

            for topic in data["topics"]:
                cleaned_topic = self.clean_topic(topic)
                diagram_parts.append(f"{cleaned_topic}\n")

        if connections:
            diagram_parts.append("connections[Related Topics]\n")
            added_connections = set()

            for topic, topic_connections in connections.items():
                for conn in topic_connections:
                    topic1, topic2 = conn["topics"]
                    clean_topic1 = self.clean_topic(topic1)
                    clean_topic2 = self.clean_topic(topic2)

                    conn_pair = tuple(sorted([clean_topic1, clean_topic2]))
                    if conn_pair not in added_connections:
                        diagram_parts.append(f"{clean_topic1} --- {clean_topic2}\n")
                        added_connections.add(conn_pair)

        return " ".join(diagram_parts)

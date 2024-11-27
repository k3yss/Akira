import os
from pathlib import Path
import re
import markdown
from bs4 import BeautifulSoup


class FileHandler:
    def __init__(self) -> None:
        """Initialize the uploaded file processor"""
        self.processed_files = {}

    def read_files(self, dir_path="uploads/"):
        """
        Read all files from the specified directory
        Returns a dictionary with filename as key and raw content as value
        """
        files = {}
        path = Path(dir_path)
        for file_path in path.glob("*.md"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    files[file_path.name] = content
            except Exception as e:
                print(f"Files not found {dir_path}")

        if not files:
            print(f"No files found in {dir_path}")

        return files

    def clean_file_text(self, file_text):
        """
        Clean file content of markdown syntax
        Removes code blocks, formatting, links, etc
        """

        # Remove code blocks
        text = re.sub(r"```[\s\S]*?```", "", file_text)
        # Remove inline code
        text = re.sub(r"`[^`]`", "", file_text)
        # Convert remaining markdown to html
        html = markdown.markdown(text)
        # Extract text from html file
        soup = BeautifulSoup(html, "html.parser")
        # get text content
        clean_text = soup.get_text()
        # remove URLs
        clean_text = re.sub(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "",
            clean_text,
        )

        # remove multiple newlines, tabs and extra spaces
        clean_text = re.sub(r"[\n\r\t]+", " ", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text)

        # remove remaining special characters
        clean_text = re.sub(r"[^\w\s.,!?]", "", clean_text)

        return clean_text.strip()

    def process_directory(self, dir_path="uploads/"):
        """
        Process all files in directory
        Returns a dictionary with filename as key and cleaned text as value
        """
        raw_files = self.read_files(dir_path)
        processed_files = {}
        for filename, content in raw_files.items():
            cleaned_text = self.clean_file_text(content)
            processed_files[filename] = cleaned_text

        self.processed_files = processed_files
        print(processed_files)
        return processed_files

    def get_file_content(self, filename):
        """Get the cleaned content of a specific file"""
        return self.processed_files.get(filename)

    def get_all_content(self):
        """Get cleaned content of all files"""
        return "\n".join(self.processed_files.values())

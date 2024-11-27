{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  languages.javascript.enable = true;
  languages.python.enable = true;
  languages.python.venv.enable = true;
  languages.python.venv.requirements = "
		flask
		flask-cors
		nltk
		gensim
		beautifulsoup4
		scikit-learn
		networkx
		numpy
		markdown
	";
  processes = {
    backend.exec = "python akira-backend/main.py";
    frontend.exec = "cd akira-frontend && npm run dev";
  };

  git-hooks.hooks = {
    black.enable = true;
    prettier.enable = true;
    nixfmt-rfc-style.enable = true;
  };
}

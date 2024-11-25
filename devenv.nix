{ pkgs, lib, config, inputs, ... }:

{
	languages.javascript.enable = true;
	languages.python.enable = true;

	packages = [ 
		pkgs.python312Packages.flask
		pkgs.python312Packages.flask-cors
	];

  processes = {
    backend.exec = "python akira-backend/main.py";
    frontend.exec = "cd akira-frontend && npm run dev";
  };

	git-hooks.hooks = {
		black.enable = true;
		prettier.enable = true;
	};
}

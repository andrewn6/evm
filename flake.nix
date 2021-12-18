{
  description = "EVM Disassmbler";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";

    mach-nix = {
      url = "github:DavHau/mach-nix/3.3.0";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
      inputs.pypi-deps-db.follows = "pypi-deps-db";
    };

    pypi-deps-db = {
      url = "github:DavHau/mach-nix/3.3.0";
    };
  };
  outputs = { self, nixpkgs, flake-utils, mach-nix, pypi-deps-db }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        python = "python39";

        inherit (nixpkgs.lib) concatStringsSep;

        pkgs = import nixpkgs { inherit system; };
        mach = import mach-nix { inherit pkgs python; };

        devRequirements = ''
          black
          flake8
          isort
          mypy
          pytest
        '';

        prodRequirements = ''
          click
          pip
        '';

        freeze = ''
          mkdir -p $out
          export out_file=$out/requirements.txt
          pip list --format=freeze > $out/requirements.txt
        '';

        devPython = mach.mkPython {
          requirements = concatStringsSep "\n" [
            prodRequirements
            devRequirements
          ];
        };

        prodPython = mach.mkPython { requirements = prodRequirements; };
      in
      rec {
        packages.prod = mach.buildPythonPackage {
          src = ./.;
          requirements = prodRequirements;
        };

        defaultPackage = packages.prod;

        packages.devRequirements = pkgs.runCommand "dev_requirements"
          {
            buildInputs = [ devPython ];
          }
          freeze;

        packages.prodRequirements = pkgs.runCommand "prod_requirements"
          {
            buildInputs = [ prodPython ];
          }
          freeze;

        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            fd
            pyright
          ] ++ [ devPython ];
        };
      });
}
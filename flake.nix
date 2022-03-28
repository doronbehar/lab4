{
  description = "Flake for all computations of Lab4 - Doron & Sarah";

  inputs = {
    # So registries will not override this
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self
  , nixpkgs
  }: let
    pkgs = import nixpkgs {
      system = "x86_64-linux";
      overlays = [
      ];
    };
    pyPkgs = p: [
      p.numpy
      p.pint
      p.matplotlib
      p.uncertainties
      p.scipy

      # For the GTK4Agg matplotlib backend, see:
      # https://matplotlib.org/stable/users/explain/backends.html
      p.pycairo
      p.pygobject3

      # For text editor
      p.jedi-language-server
      p.debugpy
    ];
    pythonEnv = pkgs.python3.withPackages(pyPkgs);
    # Meant for compiling latex text in matplotlib. Using Latex text in plots
    # requires the obscure latex package type1ec, see issues:
    # - https://github.com/matplotlib/matplotlib/issues/16911
    # - https://github.com/matplotlib/matplotlib/issues/22715#issuecomment-1080459200
    texlive = pkgs.texlive.combine {
      inherit (pkgs.texlive)
        scheme-basic
        cm-super
        type1cm
        underscore
        dvipng
        xetex
        fontspec
      ;
    };
  in {
    devShell.x86_64-linux = pkgs.mkShell {
      nativeBuildInputs = [
        pythonEnv
        texlive
        # For latex language server
        pkgs.texlab
        # For compiling our reports
        pkgs.tectonic
      ];
      MPLBACKEND = "GTK4Agg";
      GTK_THEME = "Adwaita";
    };
    packages.x86_64-linux = {
      inherit
        texlive
        pythonEnv
      ;
    };
  };
}

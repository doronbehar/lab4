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

      # For the QtAgg matplotlib backend, see:
      # https://matplotlib.org/stable/users/explain/backends.html
      p.pyqt5

      # For text editor
      p.jedi-language-server
      p.debugpy
    ];
    pythonEnv = pkgs.python3.withPackages(pyPkgs);
  in {
    devShell.x86_64-linux = pkgs.mkShell {
      nativeBuildInputs = [
        pythonEnv
        pkgs.texlab
        pkgs.tectonic
      ];
      MPLBACKEND = "QtAgg";
      QT_PLUGIN_PATH = "${pkgs.qt5.qtbase.bin}/${pkgs.qt5.qtbase.qtPluginPrefix}:${pkgs.qt5.qtwayland.bin}/${pkgs.qt5.qtbase.qtPluginPrefix}";
    };
    packages.x86_64-linux = {
      inherit pythonEnv;
    };
  };
}

{
  description = "Flake for all computations of Lab4 - Doron & Sarah";

  # To make user overrides of the nixpkgs flake not take effect
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

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
      p.pandas
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
    # requires the obscure latex package type1ec, see:
    # https://github.com/matplotlib/matplotlib/issues/16911
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
        # for matplotlib gtk4 backend
        pkgs.gtk4
        pkgs.gobject-introspection
        texlive
        # For latex language server
        pkgs.texlab
        # For compiling reports
        pkgs.tectonic
        # https://github.com/tectonic-typesetting/tectonic/issues/893#issuecomment-1116651368
        (pkgs.biber.overrideAttrs(old: {
          version = "2.16";
          src = pkgs.fetchFromGitHub {
            owner = "plk";
            repo = "biber";
            rev = "v2.16";
            sha256 = "sha256-vb/iWD/qwKik7lFPp6bmrIyl8aiMCbB2HWIKFzzCBhU=";
          };
        }))
      ];
      MPLBACKEND = "GTK4Agg";
      GTK_THEME = "Adwaita";
      XDG_DATA_DIRS = pkgs.lib.concatStringsSep ":" [
        # So we'll be able to save figures from the plot dialog
        "${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}"
        "${pkgs.gtk4}/share/gsettings-schemas/${pkgs.gtk4.name}"
        # So pdf mime types and perhaps others could be detected by 'gio open'
        # / xdg-open. TODO: Is this the best way to overcome this issue -
        # manually every time we generate a devShell?
        "${pkgs.shared-mime-info}/share"
        "${pkgs.hicolor-icon-theme}/share"
      ];
      GDK_PIXBUF_MODULE_FILE = "${pkgs.librsvg}/${pkgs.gdk-pixbuf.moduleDir}.cache";
    };
    packages.x86_64-linux = {
      inherit
        texlive
        pythonEnv
      ;
    };
  };
}

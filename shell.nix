{ pkgs, ... }:
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.graphviz
      python-pkgs.pprintpp
    ]))
    pkgs.pyright
  ];
}

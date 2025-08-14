{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;
pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages (python-pkgs: [
      python-pkgs.graphviz
    ]))
    pyright
  ];
}

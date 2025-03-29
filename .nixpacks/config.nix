{
  pkgs,
  ...
}: {
  packages = [
    pkgs.python312
    pkgs.ffmpeg
    pkgs.libGL
    pkgs.glibc
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXrender
  ];
}
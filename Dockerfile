FROM debian:latest

RUN apt update && apt upgrade -y
RUN sudo apt install ffmpeg
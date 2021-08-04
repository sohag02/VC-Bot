import ffmpeg
import pafy
import wget


def transcode(filename: str):
    out_file = f"{filename}.raw"
    a= ffmpeg.input(filename).output(
        f"{filename}.raw",
        format="s16le",
        acodec="pcm_s16le",
        ac=2,
        ar="48k",
        loglevel="error",
    ).overwrite_output().run()
    return out_file

def download_song(url,service="youtube"):
    video = pafy.new(url)

    title = video.title
    thum = video.thumb
    length = video.duration

    thum_path = wget.download(thum)

    audio = video.getbestaudio()
    path = wget.download(audio.url, out = title + ".mp3")
    caption = f"Tittle : {title}\nlength : {length}"
    return path, thum, title, length, caption


def download_and_transcode(url):
    path, thum, title, length = download_song(url)
    raw_file = transcode(path)
    return raw_file, title, length
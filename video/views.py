# Create your views here.
from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from .forms import SearchByNameForm, SearchByURLForm
from django.conf import settings
from os.path import expanduser
from pytube import YouTube
from moviepy.editor import *


def download_youtube_audio(video_url, output_path):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest quality audio stream available
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream
        audio_stream.download(output_path)

        # Get the downloaded file path
        downloaded_file_path = os.path.join(output_path, audio_stream.default_filename)

        return downloaded_file_path

    except Exception as e:
        print("Error:", e)
        return None


def convert_to_mp3(input_file_path, output_file_path):
    try:
        # Load the audio file using moviepy
        audio_clip = AudioFileClip(input_file_path)

        # Convert to MP3 format
        audio_clip.write_audiofile(output_file_path, codec='mp3')

        # Close the audio clip
        audio_clip.close()

    except Exception as e:
        print("Error:", e)


def home(request):
    search_form = SearchByNameForm(request.POST or None)
    url_form = SearchByURLForm(request.POST or None)

    if request.method == 'POST':
        if search_form.is_valid():

            youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

            query = search_form.cleaned_data['search_query']
            max_results = 10

            search_response = youtube.search().list(
                q=query,
                type='video',
                part='id,snippet',
                maxResults=max_results
            ).execute()

            videos = []
            for search_result in search_response.get('items', []):
                video = {
                    'title': search_result['snippet']['title'],
                    'thumbnail': search_result['snippet']['thumbnails']['high']['url'],
                    'video_id': search_result['id']['videoId'],
                    'embedded_url': f"https://www.youtube.com/embed/{search_result['id']['videoId']}"
                }
                videos.append(video)
            request.session['videos'] = videos
            return redirect('search')

        if url_form.is_valid():
            url = url_form.cleaned_data['url_query']
            print(url)
            request.session['url'] = url
            return redirect('download')

    return render(request, 'video/home.html', {'form1': search_form, 'form2': url_form})


def search(request):
    videos = request.session.get('videos', [])
    return render(request, 'video/search.html', {'videos': videos})


def download(request):
    url = request.session.get('url')
    video_id = url.split('/')[-1]
    video = f"https://www.youtube.com/embed/{video_id}"
    status_message = None

    if request.method == 'POST':
        download_type = request.POST.get('download_type')

        if download_type == 'mp3':
            try:
                # Replace 'YOUTUBE_VIDEO_URL' with the URL of the YouTube video you want to convert
                youtube_video_url = f'https://youtu.be/{video_id}'

                # Replace 'OUTPUT_DIRECTORY' with the path where you want to save the MP3 file
                output_directory = os.path.join(expanduser("~"), "Music")  # Adjust the directory as needed

                # Download the YouTube audio
                downloaded_audio_path = download_youtube_audio(youtube_video_url, output_directory)

                if downloaded_audio_path:
                    # Get the MP3 output file path
                    output_mp3_file_path = os.path.splitext(downloaded_audio_path)[0] + ".mp3"

                    # Convert the downloaded audio file to MP3
                    convert_to_mp3(downloaded_audio_path, output_mp3_file_path)

                    # Clean up the downloaded audio file (you can remove this if you want to keep it)
                    os.remove(downloaded_audio_path)

                    status_message = "MP3 download completed."
                else:
                    status_message = "Failed to download the YouTube audio."

            except Exception as e:
                status_message = f"Error: {e}"

        elif download_type == 'mp4':
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            yt = YouTube(video_url)
            # Get the highest resolution stream available
            video_stream = yt.streams.get_highest_resolution()

            # Replace 'DOWNLOAD_PATH' with the directory path where you want to save the video
            download_path = os.path.join(expanduser("~"), "Videos")  # Adjust the directory as needed

            # Download the video stream to the specified directory
            video_stream.download(download_path)

            status_message = "MP4 download completed."

    return render(request, 'video/download.html', {'video': video, 'status_message': status_message})


def download_v(request, video_id):
    video = f"https://www.youtube.com/embed/{video_id}"
    status_message = None

    if request.method == 'POST':
        download_type = request.POST.get('download_type')

        if download_type == 'mp3':
            try:
                # Replace 'YOUTUBE_VIDEO_URL' with the URL of the YouTube video you want to convert
                youtube_video_url = f'https://youtu.be/{video_id}'

                # Replace 'OUTPUT_DIRECTORY' with the path where you want to save the MP3 file
                output_directory = os.path.join(expanduser("~"), "Music")  # Adjust the directory as needed

                # Download the YouTube audio
                downloaded_audio_path = download_youtube_audio(youtube_video_url, output_directory)

                if downloaded_audio_path:
                    # Get the MP3 output file path
                    output_mp3_file_path = os.path.splitext(downloaded_audio_path)[0] + ".mp3"

                    # Convert the downloaded audio file to MP3
                    convert_to_mp3(downloaded_audio_path, output_mp3_file_path)

                    # Clean up the downloaded audio file (you can remove this if you want to keep it)
                    os.remove(downloaded_audio_path)

                    status_message = "MP3 download completed."
                else:
                    status_message = "Failed to download the YouTube audio."

            except Exception as e:
                status_message = f"Error: {e}"

        elif download_type == 'mp4':
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            yt = YouTube(video_url)
            # Get the highest resolution stream available
            video_stream = yt.streams.get_highest_resolution()

            # Replace 'DOWNLOAD_PATH' with the directory path where you want to save the video
            download_path = os.path.join(expanduser("~"), "Videos")  # Adjust the directory as needed

            # Download the video stream to the specified directory
            video_stream.download(download_path)

            status_message = "MP4 download completed."

    return render(request, 'video/download.html', {'video': video, 'status_message': status_message})

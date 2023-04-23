#!/usr/bin/env python

"""
The very cool clipper, thanks Chopper Script
Gets an open project and chops clips based on track 1 volume.
"""

VIDEO_EXTENSIONS_TO_CHOP = (".mkv", ".avi")
AUDIO_THRESHOLD = 0.005
BUFFER_FRAMES = 5
PICKUP_FRAMES = 5
CONTINUITY_FRAMES = 20


import sys
import DaVinciResolveScript as Script
from moviepy.editor import VideoFileClip

def mark_audio_levels(
        video_location: str, 
        audio_threshold: float = AUDIO_THRESHOLD, 
        buffer_frames: int = BUFFER_FRAMES,
        pickup_frames: int = PICKUP_FRAMES,
        continuity_frames: int = CONTINUITY_FRAMES,
    ):
    video = VideoFileClip(video_location)
    audio = video.audio

    consecutive = 0
    current_frame = 0
    continuity = continuity_frames
    start_frame = 0
    for frame in audio.iter_frames(fps = video.fps):
        current_frame += 1
        if abs(frame.mean()) > audio_threshold:
            if consecutive == 0:
                start_frame = current_frame
            consecutive += 1
            continuity = continuity_frames
        else:
            if consecutive >= 1 and continuity > 0:
                continuity -= 1
            else:
                if consecutive > pickup_frames:
                    start = max(start_frame - buffer_frames, 0)
                    end = (current_frame + buffer_frames) - continuity_frames
                    print(f"{start} -> {end}")
                    yield (start, end)
                consecutive = 0
                continuity = continuity_frames

resolve = Script.scriptapp("Resolve")
manager = resolve.GetProjectManager()
project = manager.GetCurrentProject()

print("Connected to resolve, scanning loaded media.")

media = project.GetMediaPool()

print("Linked to media pool, loading videos from root.")

folder = media.GetRootFolder()

for clip in folder.GetClipList():
    if str.endswith(clip.GetName(), VIDEO_EXTENSIONS_TO_CHOP):
        name = clip.GetName()
        print("Creating timeline for chopped clip")
        timeline = media.CreateEmptyTimeline(f"Chopped {name}")

        print("Loaded " + name + ", chopping.")


        frames = mark_audio_levels(clip.GetClipProperty("File Path"))
        for (start, end) in frames:
            sub_clip = {
                "mediaPoolItem": clip,
                "startFrame": start,
                "endFrame": end,
            }
            media.AppendToTimeline([sub_clip])

        manager.SaveProject()
        
    
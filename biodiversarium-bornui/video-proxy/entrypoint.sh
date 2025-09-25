#!/bin/sh

cvlc rtsp://194.167.19.10:1433/1/h264major --sout '#transcode{vcodec=theo,vb=800,scale=1,width=1920,height=1080,acodec=none,scodec=none}:http{dst=:8001/in.ogg}' &
cvlc rtsp://admin:Imerir66@194.167.19.10:554/11 --sout '#transcode{vcodec=theo,vb=800,scale=1,width=1920,height=1080,acodec=none,scodec=none}:http{dst=:8002/out.ogg}'

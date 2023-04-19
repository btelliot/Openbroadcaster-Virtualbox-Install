#!/bin/bash

#ffmpeg -protocol_whitelist file,crypto,udp,rtp -i /home/obsuser/livewire.sdp -acodec libmp3lame -ab 64k -ac 2 -content_type audio/mpeg -f mp3 icecast://source:1c3c4stS0uRc3@localhost:8000/cjuc

ffmpeg -protocol_whitelist file,crypto,udp,rtp -i /home/obsuser/livewire.sdp -c:a libmp3lame -ab 256k -ac 2 -content_type audio/mp3 -f mp3 icecast://source:EHgu04uRv6Z@localhost:8000/cjuc

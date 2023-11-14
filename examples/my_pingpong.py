import pylibdatachannel 
import threading
e=threading.Event()

pylibdatachannel.init_logger(pylibdatachannel.LogLevel.LOG_ERROR)

sender=pylibdatachannel.PeerConnection()
receiver=pylibdatachannel.PeerConnection()

track = sender.add_track(
    b"\n".join(
        [b"audio 9 UDP/TLS/RTP/SAVPF 0",
         b"c=IN IP4 0.0.0.0",
         b"a=rtpmap:0 PCMU/8000",
         b"a=mid:audio",
         b"a=sendrecv",
         b"a=rtcp:9 IN IP4 0.0.0.0",
         b'a=msid:- audio-track-8247152b-ff6a-43f9-98ce-f5815fae6b4d',
         b"a=ssrc:4125531231 cname:iP6DXCUIB/7GAsxT",
         b"a=ssrc:4125531231 msid:- audio-track-8247152b-ff6a-43f9-98ce-f5815fae6b4d"
        ]
    )
)

def on_sender_gathering_state_change(state):
    if state == pylibdatachannel.GatheringState.GATHERING_COMPLETE:
        def on_receiver_gathering_state_change(state):
            if state == pylibdatachannel.GatheringState.GATHERING_COMPLETE:
                sender.set_remote_description(receiver.local_description.encode(), b'answer')
        def on_b_track(track):
            track.message_callback=lambda x, y: print("pong", x) or e.set()
            
        receiver.gathering_state_change_callback = on_receiver_gathering_state_change
        receiver.track_callback=on_b_track
        receiver.set_remote_description(sender.local_description.encode(), b'offer')

        def on_sender_track_open():
            example_rtp_packet = b"\x80\x80\n\xa8\xbd.\x0b\x1d/(\xfe\x9cbY[TV_`ZWWZ[[\\YXXW]_^do\xf8\xf7mge]^biknkfg_\\Z^bWOONLLKHHHHIJNQNMLLOPRTWTOSZagillf__]["
            track.send_message(example_rtp_packet, len(example_rtp_packet))
            print("ping")
        track.open_callback=on_sender_track_open

sender.gathering_state_change_callback = on_sender_gathering_state_change
sender.set_local_description()

e.wait()

import React, { useEffect, useRef } from 'react';
import Hls from 'hls.js';

const VideoPlayer = ({ videoUrl }) => {
    const videoRef = useRef(null);

    useEffect(() => {
        if (!videoUrl) return;

        if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource(videoUrl);
            hls.attachMedia(videoRef.current);

            hls.on(Hls.Events.MANIFEST_PARSED, () => {
                videoRef.current.play();
            });

            hls.on(Hls.Events.ERROR, (event, data) => {
                console.error('HLS error:', data);
            });

            return () => {
                hls.destroy();
            };
        } else if (videoRef.current.canPlayType('application/vnd.apple.mpegurl')) {
            // Native support for HLS (e.g., Safari)
            videoRef.current.src = videoUrl;
            videoRef.current.play();
        }
    }, [videoUrl]);

    return (
        <video
            ref={videoRef}
            controls
            style={{ width: '100%', height: 'auto' }}
        />
    );
};

export default VideoPlayer;

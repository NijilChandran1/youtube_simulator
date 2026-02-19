import { Component, ElementRef, Input, ViewChild, AfterViewInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VideoService } from '../../services/video.service';

@Component({
    selector: 'app-video-player',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './video-player.component.html',
    styleUrls: ['./video-player.component.scss']
})
export class VideoPlayerComponent implements AfterViewInit, OnDestroy {
    @ViewChild('videoPlayer') videoElement!: ElementRef<HTMLVideoElement>;
    @Input() src: string = '';

    constructor(private videoService: VideoService) { }

    ngAfterViewInit() {
        const video = this.videoElement.nativeElement;

        // Register video element with service for smooth clock updates
        this.videoService.registerVideoElement(video);

        video.ontimeupdate = () => {
            this.videoService.updateTime(video.currentTime);
        };

        video.onloadedmetadata = () => {
            this.videoService.updateDuration(video.duration);
        };

        video.onplay = () => this.videoService.updateState('playing');
        video.onpause = () => this.videoService.updateState('paused');
        video.onended = () => this.videoService.updateState('ended');

        this.videoService.playCommand$.subscribe(shouldPlay => {
            if (shouldPlay) {
                console.log("Received Play Command. Attempting to play...");
                video.play()
                    .then(() => console.log("Video playing successfully."))
                    .catch(e => {
                        console.error("Auto-play failed:", e);
                        // Fallback: If auto-play blocked, maybe mute and try again?
                        if (e.name === 'NotAllowedError') {
                            console.warn("Auto-play blocked. Attempting muted play.");
                            video.muted = true;
                            video.play().catch(e2 => console.error("Muted play failed:", e2));
                        }
                    });
            } else {
                video.pause();
                video.currentTime = 0; // Reset to start? "original status"
            }
        });
    }

    ngOnDestroy() {
        // Cleanup if needed
    }

    play() {
        this.videoElement.nativeElement.play();
    }

    pause() {
        this.videoElement.nativeElement.pause();
    }

    preventPause(event: Event) {
        event.preventDefault();
        // optionally ensure it keeps playing if they clicked it
        // this.videoElement.nativeElement.play();
    }
}

import { Component, Input, OnInit, OnDestroy, OnChanges, SimpleChanges, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VideoService } from '../../services/video.service';
import { Subscription } from 'rxjs';

@Component({
    selector: 'app-clock-overlay',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './clock-overlay.component.html',
    styleUrls: ['./clock-overlay.component.scss']
})
export class ClockOverlayComponent implements OnInit, OnDestroy, OnChanges {
    @Input() startTimeISO: string = ''; // e.g. "2026-02-11T19:00:00"

    displayTime: string = "00:00:00.000";
    private sub: Subscription | null = null;
    private videoElementSub: Subscription | null = null;
    private playbackStateSub: Subscription | null = null;
    private startTimestamp: number = 0;

    // Animation frame tracking for smooth updates
    private animationFrameId: number | null = null;
    private videoElement: HTMLVideoElement | null = null;
    private isPlaying: boolean = false;

    constructor(
        private videoService: VideoService,
        private cdr: ChangeDetectorRef
    ) { }

    ngOnInit() {
        this.updateStartTimestamp();

        // Subscribe to video element
        this.videoElementSub = this.videoService.videoElement$.subscribe(element => {
            this.videoElement = element;
            if (element && !this.animationFrameId) {
                this.startClockAnimation();
            }
        });

        // Subscribe to playback state
        this.playbackStateSub = this.videoService.playbackState$.subscribe(state => {
            this.isPlaying = (state === 'playing');
            console.log('Clock overlay - playback state changed:', state);
        });

        // Keep existing subscription as fallback
        this.sub = this.videoService.currentTime$.subscribe(currentTime => {
            // Fallback if animation frame isn't running
            if (!this.animationFrameId) {
                this.updateClock(currentTime);
            }
        });
    }

    ngOnChanges(changes: SimpleChanges) {
        if (changes['startTimeISO']) {
            this.updateStartTimestamp();
        }
    }

    private startClockAnimation() {
        console.log('Starting clock animation loop');
        const animate = () => {
            if (this.videoElement && this.isPlaying) {
                const videoTime = this.videoElement.currentTime;
                this.updateClock(videoTime);
            }
            this.animationFrameId = requestAnimationFrame(animate);
        };

        if (!this.animationFrameId) {
            this.animationFrameId = requestAnimationFrame(animate);
        }
    }

    updateStartTimestamp() {
        if (this.startTimeISO) {
            this.startTimestamp = new Date(this.startTimeISO).getTime();
        } else {
            this.startTimestamp = Date.now(); // Fallback
        }
        console.log("Clock Start Time updated to:", new Date(this.startTimestamp).toISOString());
    }

    updateClock(videoTimeSeconds: number) {
        const currentMs = this.startTimestamp + (videoTimeSeconds * 1000);
        const date = new Date(currentMs);
        // Format HH:MM:SS.mmm
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');
        const ms = date.getMilliseconds().toString().padStart(3, '0');
        this.displayTime = `${hours}:${minutes}:${seconds}.${ms}`;

        // Force Angular to detect changes from RAF
        this.cdr.detectChanges();
    }

    ngOnDestroy() {
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
        this.sub?.unsubscribe();
        this.videoElementSub?.unsubscribe();
        this.playbackStateSub?.unsubscribe();
    }
}

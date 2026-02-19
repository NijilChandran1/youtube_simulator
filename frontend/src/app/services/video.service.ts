import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class VideoService {
    private currentTimeSubject = new BehaviorSubject<number>(0);
    currentTime$ = this.currentTimeSubject.asObservable();

    private durationSubject = new BehaviorSubject<number>(0);
    duration$ = this.durationSubject.asObservable();

    private playbackStateSubject = new BehaviorSubject<'playing' | 'paused' | 'ended'>('paused');
    playbackState$ = this.playbackStateSubject.asObservable();

    // NEW: Video element reference for smooth clock updates
    private videoElementSubject = new BehaviorSubject<HTMLVideoElement | null>(null);
    videoElement$ = this.videoElementSubject.asObservable();

    constructor() { }

    updateTime(time: number) {
        this.currentTimeSubject.next(time);
    }

    updateDuration(duration: number) {
        this.durationSubject.next(duration);
    }

    updateState(state: 'playing' | 'paused' | 'ended') {
        this.playbackStateSubject.next(state);
    }

    // NEW: Register video element for direct access
    registerVideoElement(element: HTMLVideoElement) {
        this.videoElementSubject.next(element);
    }

    private playCommandSubject = new BehaviorSubject<boolean>(false);
    playCommand$ = this.playCommandSubject.asObservable();

    playVideo() {
        this.playCommandSubject.next(true);
    }

    pauseVideo() {
        this.playCommandSubject.next(false);
    }
}

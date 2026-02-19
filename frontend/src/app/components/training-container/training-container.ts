import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { VideoPlayerComponent } from '../video-player/video-player.component';
import { ClockOverlayComponent } from '../clock-overlay/clock-overlay.component';
import { ControlPanelComponent } from '../control-panel/control-panel.component';
import { FeedbackDisplayComponent } from '../feedback-display/feedback-display.component';
import { SessionStatsComponent } from '../session-stats/session-stats';
import { AnalyticsDrawerComponent } from '../analytics-drawer/analytics-drawer';
import { ApiService, Video } from '../../services/api.service';
import { VideoService } from '../../services/video.service';
import { FeedbackResponse } from '../../models/feedback.model';

@Component({
  selector: 'app-training-container',
  standalone: true,
  imports: [
    CommonModule,
    VideoPlayerComponent,
    ClockOverlayComponent,
    ControlPanelComponent,
    FeedbackDisplayComponent,
    SessionStatsComponent,
    AnalyticsDrawerComponent
  ],
  templateUrl: './training-container.html',
  styleUrls: ['./training-container.scss']
})
export class TrainingContainerComponent implements OnInit {
  sessionId = 0;
  videoSrc = '/assets/video.mp4';
  startTimeISO = "2026-02-11T19:00:00";

  feedbackList: FeedbackResponse[] = [];
  currentTime: number = 0;
  isPlaying: boolean = false;
  isFeedbackOpen: boolean = false;
  isAnalyticsOpen: boolean = false;
  isStarting: boolean = false;
  actionLog: { message: string, isError: boolean, timestamp: string }[] = [];
  lastFeedback: { attribute: string; accuracy: string } | null = null;

  selectedVideo: Video | null = null;
  eventButtons: { label: string, key: string }[] = [];

  constructor(
    private apiService: ApiService,
    private videoService: VideoService,
    private cd: ChangeDetectorRef,
    private router: Router
  ) {
    // Get selected video from navigation state
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras?.state) {
      this.selectedVideo = navigation.extras.state['selectedVideo'];
    }

    this.videoService.currentTime$.subscribe(t => this.currentTime = t);
    this.videoService.playbackState$.subscribe(state => {
      this.isPlaying = state === 'playing';
    });
  }

  ngOnInit() {
    // If no video selected, redirect back to selection
    if (!this.selectedVideo) {
      this.router.navigate(['/']);
      return;
    }

    // Set video source and broadcast time from selected video
    this.videoSrc = `/assets/${this.selectedVideo.file_path}`;
    this.startTimeISO = this.selectedVideo.broadcast_start_time;

    console.log('Training initialized with video:', this.selectedVideo);

    // Fetch dynamic event attributes
    this.apiService.getVideoAttributes(this.selectedVideo.video_id).subscribe({
      next: (attributes) => {
        console.log('Fetched attributes:', attributes);
        this.eventButtons = attributes.map((attr, index) => ({
          label: attr,
          key: (index + 1).toString()
        }));
      },
      error: (err) => console.error('Failed to fetch attributes:', err)
    });
  }

  toggleFeedback() {
    this.isFeedbackOpen = !this.isFeedbackOpen;
  }

  toggleAnalytics() {
    this.isAnalyticsOpen = !this.isAnalyticsOpen;
  }

  onEventLogged(attribute: string) {
    if (this.sessionId === 0) {
      this.addToLog("Please Start Session first!", true);
      return;
    }

    const capturedAttribute = attribute;
    const startMs = new Date(this.startTimeISO).getTime();
    const currentMs = startMs + (this.currentTime * 1000);
    const date = new Date(currentMs);

    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    const ms = date.getMilliseconds().toString().padStart(3, '0');
    const userLiveTime = `${hours}:${minutes}:${seconds}.${ms}`;

    console.log(`Logging event: ${capturedAttribute} at ${this.currentTime}s (${userLiveTime})`);
    this.addToLog(capturedAttribute, false, userLiveTime);

    this.apiService.logEvent(
      this.sessionId,
      capturedAttribute,
      this.currentTime,
      userLiveTime,
      this.currentTime
    ).subscribe({
      next: (response) => {
        console.log('Feedback received:', response);

        // Create new array reference to trigger change detection
        this.feedbackList = [response, ...this.feedbackList];

        // Update lastFeedback to trigger button animation
        this.lastFeedback = {
          attribute: response.clicked_attribute,
          accuracy: response.accuracy_level
        };

        this.cd.detectChanges();
      },
      error: (err) => {
        console.error('Error logging event:', err);
        if (this.actionLog.length > 0 && this.actionLog[0].message === capturedAttribute) {
          this.actionLog[0].message = `Error: ${capturedAttribute}`;
          this.actionLog[0].isError = true;
        }
      }
    });
  }

  addToLog(message: string, isError: boolean, customTimestamp?: string) {
    const timestamp = customTimestamp || new Date().toLocaleTimeString();
    this.actionLog.unshift({ message, isError, timestamp });
    if (this.actionLog.length > 10) {
      this.actionLog.pop();
    }
  }

  startSession() {
    this.isStarting = true;
    this.feedbackList = [];

    // Use selected video ID if available
    const videoId = this.selectedVideo?.video_id;

    this.apiService.startSession("guest@example.com", videoId).subscribe({
      next: (res) => {
        console.log("Session started:", res);
        this.sessionId = res.session_id;

        let startTimeDisplay = new Date().toLocaleTimeString();
        if (res.broadcast_start_time) {
          this.startTimeISO = res.broadcast_start_time;
          const d = new Date(this.startTimeISO);
          startTimeDisplay = d.toTimeString().split(' ')[0];
        }

        this.addToLog(`Session Started (ID: ${this.sessionId})`, false, startTimeDisplay);
        this.videoService.playVideo();
        this.isStarting = false;
        this.cd.detectChanges();
      },
      error: (err) => {
        console.error("Failed to start session:", err);
        this.addToLog("Failed to Start Session", true);
        this.isStarting = false;
        this.cd.detectChanges();
      }
    });
  }

  endSession() {
    console.log("Ending session...");
    this.sessionId = 0;
    this.actionLog = [];
    this.videoService.pauseVideo();
  }
}

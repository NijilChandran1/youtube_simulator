import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService, Video } from '../../services/api.service';

interface Workflow {
  id: string;
  name: string;
  isActive: boolean;
}

@Component({
  selector: 'app-video-selection',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './video-selection.html',
  styleUrls: ['./video-selection.scss']
})
export class VideoSelectionComponent implements OnInit {
  // Configurable workflow list - easily update here
  workflows: Workflow[] = [
    { id: 'workflow1', name: 'Workflow 1 - Identify Events', isActive: true },
    { id: 'workflow2', name: 'Workflow 2 - Update Schedules', isActive: false }
  ];

  selectedWorkflow: string = 'workflow1'; // Default to Workflow 1
  videos: Video[] = [];
  selectedVideo: Video | null = null;
  isLoading = true;
  errorMessage = '';

  constructor(
    private apiService: ApiService,
    private router: Router,
    private cd: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.loadVideos();
  }

  onWorkflowChange(event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    this.selectedWorkflow = selectElement.value;

    // Future: Filter videos based on selected workflow
    console.log('Selected workflow:', this.selectedWorkflow);
  }

  loadVideos() {
    this.isLoading = true;
    console.log('VideoSelection: Starting to load videos...');

    this.apiService.getVideoList().subscribe({
      next: (videos) => {
        console.log('VideoSelection: Raw API response:', videos);
        this.videos = videos;
        this.isLoading = false;
        console.log('VideoSelection: Videos assigned to property. Count:', this.videos.length);
        this.cd.detectChanges(); // Force update
      },
      error: (err) => {
        console.error('VideoSelection: Error loading videos:', err);
        this.errorMessage = 'Failed to load videos. Please try again.';
        this.isLoading = false;
        this.cd.detectChanges();
      }
    });
  }

  onVideoSelect(event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    const videoId = selectElement.value;

    if (videoId) {
      this.selectedVideo = this.videos.find(v => v.video_id === videoId) || null;

      if (this.selectedVideo) {
        console.log('Selected video:', this.selectedVideo);
        // Navigate to training screen with selected video data
        this.router.navigate(['/training'], {
          state: { selectedVideo: this.selectedVideo }
        });
      }
    }
  }
}

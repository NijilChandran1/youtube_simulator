import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FeedbackResponse } from '../../models/feedback.model';

@Component({
  selector: 'app-session-stats',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './session-stats.html',
  styleUrls: ['./session-stats.scss']
})
export class SessionStatsComponent implements OnChanges {
  @Input() feedbackList: FeedbackResponse[] = [];
  @Input() sessionActive: boolean = false;

  totalEvents: number = 0;
  perfectCount: number = 0;
  acceptableCount: number = 0;
  missCount: number = 0;
  falsePositiveCount: number = 0;
  accuracyPercentage: number = 0;

  ngOnChanges(changes: SimpleChanges) {
    if (changes['feedbackList']) {
      this.calculateStats();
    }
  }

  private calculateStats() {
    this.totalEvents = this.feedbackList.length;
    this.perfectCount = this.feedbackList.filter(f => f.accuracy_level === 'perfect').length;
    this.acceptableCount = this.feedbackList.filter(f => f.accuracy_level === 'acceptable').length;
    this.missCount = this.feedbackList.filter(f => f.accuracy_level === 'miss').length;
    this.falsePositiveCount = this.feedbackList.filter(f => f.accuracy_level === 'false_positive').length;

    // Calculate accuracy (perfect + acceptable / total)
    const successfulEvents = this.perfectCount + this.acceptableCount;
    this.accuracyPercentage = this.totalEvents > 0
      ? Math.round((successfulEvents / this.totalEvents) * 100)
      : 0;
  }

  getAccuracyClass(): string {
    if (this.accuracyPercentage >= 80) return 'excellent';
    if (this.accuracyPercentage >= 60) return 'good';
    if (this.accuracyPercentage >= 40) return 'fair';
    return 'poor';
  }
}

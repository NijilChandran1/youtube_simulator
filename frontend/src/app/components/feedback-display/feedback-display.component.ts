import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FeedbackResponse } from '../../models/feedback.model';

@Component({
    selector: 'app-feedback-display',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './feedback-display.component.html',
    styleUrls: ['./feedback-display.component.scss']
})
export class FeedbackDisplayComponent {
    @Input() feedbackList: FeedbackResponse[] = [];

    // Sort feedback in ascending order by time (earliest first)
    get sortedFeedbackList(): FeedbackResponse[] {
        return [...this.feedbackList].sort((a, b) => {
            // Compare timestamps as strings (HH:MM:SS.mmm format)
            return a.user_clicked_time.localeCompare(b.user_clicked_time);
        });
    }

    getAccuracyClass(accuracy: string): string {
        switch (accuracy) {
            case 'perfect': return 'badge-perfect';
            case 'acceptable': return 'badge-ok';
            case 'miss': return 'badge-miss';
            case 'false_positive': return 'badge-false';
            default: return '';
        }
    }

    // Convert technical terms to user-friendly labels
    getAccuracyLabel(accuracy: string): string {
        switch (accuracy) {
            case 'perfect': return '✓ Perfect';
            case 'acceptable': return '✓ Good';
            case 'miss': return '✗ Missed';
            case 'false_positive': return '✗ Wrong Event';
            default: return accuracy;
        }
    }

    // Generate user-friendly feedback message
    getFeedbackMessage(item: FeedbackResponse): string {
        const clickedAttr = item.clicked_attribute;
        const expectedAttr = item.ground_truth?.clue_description;

        switch (item.accuracy_level) {
            case 'perfect':
                return `Great! You caught "${clickedAttr}" at the perfect time.`;
            case 'acceptable':
                return `Good! You caught "${clickedAttr}" close to the right time.`;
            case 'miss':
                return `You missed "${expectedAttr}". Try to click when you see it.`;
            case 'false_positive':
                return `"${clickedAttr}" wasn't showing at this time. Watch carefully!`;
            default:
                return '';
        }
    }

    // Format time difference in seconds
    getTimeDifferenceText(diffMs: number): string {
        if (diffMs === 0) return '';
        const diffSec = (Math.abs(diffMs) / 1000).toFixed(2);
        const direction = diffMs > 0 ? 'late' : 'early';
        return `${diffSec}s ${direction}`;
    }
}

import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

interface SessionHistory {
    session_id: number;
    created_at: string;
    video_name: string;
    total_events: number;
    perfect_count: number;
    good_count: number;
    missed_count: number;
    wrong_count: number;
    accuracy_percentage: number;
}

@Component({
    selector: 'app-analytics-drawer',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './analytics-drawer.html',
    styleUrls: ['./analytics-drawer.scss']
})
export class AnalyticsDrawerComponent implements OnInit {
    @Input() isOpen: boolean = false;
    @Output() close = new EventEmitter<void>();

    sessionHistory: SessionHistory[] = [];
    isLoading: boolean = false;
    bestSession: SessionHistory | null = null;
    latestSession: SessionHistory | null = null;
    averageAccuracy: number = 0;

    constructor(private apiService: ApiService) { }

    ngOnInit() {
        this.loadSessionHistory();
    }

    closeDrawer() {
        this.close.emit();
    }

    loadSessionHistory() {
        this.isLoading = true;
        this.apiService.getSessionHistory().subscribe({
            next: (history) => {
                this.sessionHistory = history;
                this.calculateStats();
                this.isLoading = false;
            },
            error: (err) => {
                console.error('Failed to load session history:', err);
                this.isLoading = false;
            }
        });
    }

    calculateStats() {
        if (this.sessionHistory.length === 0) return;

        // Best session (highest accuracy)
        this.bestSession = this.sessionHistory.reduce((best, current) =>
            current.accuracy_percentage > best.accuracy_percentage ? current : best
        );

        // Latest session
        this.latestSession = this.sessionHistory[0];

        // Average accuracy
        const total = this.sessionHistory.reduce((sum, s) => sum + s.accuracy_percentage, 0);
        this.averageAccuracy = Math.round(total / this.sessionHistory.length);
    }

    formatDate(dateString: string): string {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
}

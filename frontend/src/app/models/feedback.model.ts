export interface FeedbackResponse {
    attempt_id: number;
    clicked_attribute: string;  // The attribute the user clicked
    user_clicked_time: string;  // When the user clicked (live clock time)
    accuracy_level: 'perfect' | 'acceptable' | 'miss' | 'false_positive';
    time_difference_ms: number;
    ground_truth?: {
        timestamp_seconds: number;
        live_clock_time: string;
        clue_description: string;
    };
    ai_feedback?: string;
}

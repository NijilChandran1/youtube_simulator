export interface GroundTruthEvent {
    attribute: string;
    timestamp_seconds: number;
    live_clock_time: string;
    clue_description: string;
    confidence_score: number;
}

export interface VideoAnalysisResult {
    video_id: string;
    duration_seconds: number;
    broadcast_start_time: string;
    events: GroundTruthEvent[];
    analysis_status: string;
}

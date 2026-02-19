import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FeedbackResponse } from '../models/feedback.model';
import { VideoAnalysisResult } from '../models/event.model';

export interface Video {
    id: number;
    video_id: string;
    title: string;
    duration_seconds: number;
    file_path: string;
    broadcast_start_time: string;
}

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private apiUrl = '/api';

    constructor(private http: HttpClient) { }

    analyzeVideo(file: File, startTime: string, attributes: string): Observable<VideoAnalysisResult> {
        const formData = new FormData();
        formData.append('video_file', file);
        formData.append('broadcast_start_time', startTime);
        formData.append('attribute_types', attributes);
        return this.http.post<VideoAnalysisResult>(`${this.apiUrl}/videos/analyze`, formData);
    }

    logEvent(sessionId: number, attribute: string, userTime: number, userLiveTime: string, videoTime: number): Observable<FeedbackResponse> {
        return this.http.post<FeedbackResponse>(`${this.apiUrl}/events/log`, {
            session_id: sessionId,
            attribute,
            user_timestamp_seconds: userTime,
            user_live_clock_time: userLiveTime,
            video_timestamp_seconds: videoTime
        });
    }

    startSession(userEmail: string = "guest@example.com", videoId?: string): Observable<any> {
        return this.http.post(`${this.apiUrl}/sessions/start`, {
            user_email: userEmail,
            video_id: videoId
        });
    }

    getVideoList(): Observable<Video[]> {
        return this.http.get<Video[]>(`${this.apiUrl}/videos/list`);
    }

    getSessionHistory(userEmail: string = "guest@example.com"): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/sessions/history?user_email=${userEmail}`);
    }

    getVideoAttributes(videoId: string): Observable<string[]> {
        return this.http.get<string[]>(`${this.apiUrl}/videos/${videoId}/attributes`);
    }
}

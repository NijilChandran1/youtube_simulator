import { Routes } from '@angular/router';
import { VideoSelectionComponent } from './components/video-selection/video-selection';
import { TrainingContainerComponent } from './components/training-container/training-container';

export const routes: Routes = [
    { path: '', component: VideoSelectionComponent },
    { path: 'training', component: TrainingContainerComponent },
    { path: '**', redirectTo: '' }
];

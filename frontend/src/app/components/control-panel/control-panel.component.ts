import { Component, EventEmitter, Output, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-control-panel',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './control-panel.component.html',
    styleUrls: ['./control-panel.component.scss']
})
export class ControlPanelComponent implements OnChanges {
    @Input() isEnabled: boolean = false;
    @Input() lastFeedback: { attribute: string; accuracy: string } | null = null;
    @Output() eventLogged = new EventEmitter<string>();

    // Track animation states for each button
    buttonStates: Map<string, 'idle' | 'success' | 'error'> = new Map();

    ngOnChanges(changes: SimpleChanges) {
        if (changes['isEnabled']) {
            console.log('ControlPanel isEnabled changed:', changes['isEnabled'].currentValue);
        }

        // Trigger animation when feedback changes
        if (changes['lastFeedback'] && this.lastFeedback) {
            this.triggerFeedbackAnimation(this.lastFeedback.attribute, this.lastFeedback.accuracy);
        }
    }

    @Input() buttons: { label: string, key: string }[] = [
        { label: 'Main Logo', key: '1' },
        { label: 'Copyright', key: '2' },
        { label: 'Post-Game Start', key: '3' },
        { label: 'Scoreboard', key: '4' },
        { label: 'Replay Graphic', key: '5' }
    ];

    logEvent(attribute: string) {
        this.eventLogged.emit(attribute);
    }

    getButtonState(label: string): string {
        return this.buttonStates.get(label) || 'idle';
    }

    private triggerFeedbackAnimation(attribute: string, accuracy: string) {
        const state = (accuracy === 'perfect' || accuracy === 'acceptable') ? 'success' : 'error';
        this.buttonStates.set(attribute, state);

        // Reset after animation completes
        setTimeout(() => {
            this.buttonStates.set(attribute, 'idle');
        }, 600);
    }
}

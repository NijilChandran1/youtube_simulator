import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoSelection } from './video-selection';

describe('VideoSelection', () => {
  let component: VideoSelection;
  let fixture: ComponentFixture<VideoSelection>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VideoSelection]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VideoSelection);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainingContainer } from './training-container';

describe('TrainingContainer', () => {
  let component: TrainingContainer;
  let fixture: ComponentFixture<TrainingContainer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TrainingContainer]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TrainingContainer);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

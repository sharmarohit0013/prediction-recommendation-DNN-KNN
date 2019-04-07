import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RetrainModelComponent } from './retrain-model.component';

describe('RetrainModelComponent', () => {
  let component: RetrainModelComponent;
  let fixture: ComponentFixture<RetrainModelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RetrainModelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RetrainModelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

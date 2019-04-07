import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { IncorrectSolutionComponent } from './incorrect-solution.component';

describe('IncorrectSolutionComponent', () => {
  let component: IncorrectSolutionComponent;
  let fixture: ComponentFixture<IncorrectSolutionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ IncorrectSolutionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IncorrectSolutionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

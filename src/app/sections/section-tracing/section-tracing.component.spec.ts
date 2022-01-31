import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SectionTracingComponent } from './section-tracing.component';

describe('SectionTracingComponent', () => {
  let component: SectionTracingComponent;
  let fixture: ComponentFixture<SectionTracingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SectionTracingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SectionTracingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

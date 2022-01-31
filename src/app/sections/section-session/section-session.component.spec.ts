import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SectionSessionComponent } from './section-session.component';

describe('SectionSessionComponent', () => {
  let component: SectionSessionComponent;
  let fixture: ComponentFixture<SectionSessionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SectionSessionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SectionSessionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

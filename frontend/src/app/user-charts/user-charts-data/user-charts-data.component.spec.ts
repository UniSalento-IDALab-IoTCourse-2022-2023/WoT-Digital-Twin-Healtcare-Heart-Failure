import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserChartsDataComponent } from './user-charts-data.component';

describe('UserChartsDataComponent', () => {
  let component: UserChartsDataComponent;
  let fixture: ComponentFixture<UserChartsDataComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UserChartsDataComponent]
    });
    fixture = TestBed.createComponent(UserChartsDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

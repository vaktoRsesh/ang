import { Routes } from '@angular/router';

import { SectionDataComponent } from './app/sections/section-data/section-data.component';
import { SectionSessionComponent } from './app/sections/section-session/section-session.component';
import { SectionTracingComponent } from './app/sections/section-tracing/section-tracing.component';

export const appRoutes: Routes = [
    { path: 'data', component: SectionDataComponent },
    { path: 'session', component: SectionSessionComponent },
    { path: 'tracing', component: SectionTracingComponent },

    { path: '', redirectTo: '/session', pathMatch: 'full' }
];



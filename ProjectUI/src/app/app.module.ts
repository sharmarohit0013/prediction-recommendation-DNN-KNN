import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { HomePageComponent } from './home-page/home-page.component';
import { AboutPageComponent } from './about-page/about-page.component';
import { RecommendationListComponent } from './recommendation-list/recommendation-list.component';

import { RouterModule, Routes } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HttpService } from './service/http.service';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';

import {MatDialogModule} from "@angular/material";
import { IncorrectSolutionComponent } from './incorrect-solution/incorrect-solution.component';
import { RetrainModelComponent } from './retrain-model/retrain-model.component';

const appRoutes:Routes = [
  {path:'HomePage', component:HomePageComponent},
  {path:'AboutPage', component:AboutPageComponent},
  {path: '**', redirectTo:'/HomePage', pathMatch:'full'}
]
@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    AboutPageComponent,
    RecommendationListComponent,
    IncorrectSolutionComponent,
    RetrainModelComponent
    
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    HttpClientModule,
    BrowserAnimationsModule,
    MatDialogModule,
    FormsModule
    
  ],
    entryComponents: [
      RecommendationListComponent,
      IncorrectSolutionComponent,
      RetrainModelComponent,
    ],
  providers: [HttpService],
  bootstrap: [AppComponent]
})
export class AppModule { }
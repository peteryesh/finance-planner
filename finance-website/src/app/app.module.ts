import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';

import { UserLoginComponent  } from 'src/components/user-login/user-login.component';
import { AccountComponent } from 'src/components/account/account.component';
import { UserMainComponent } from 'src/components/user-main/user-main.component';

@NgModule({
  declarations: [
    AppComponent,
    UserLoginComponent,
    AccountComponent,
    UserMainComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule.forRoot([
    ]),
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

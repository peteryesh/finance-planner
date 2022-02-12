import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';

import { UserLoginComponent  } from 'src/components/user-login/user-login.component';
import { UserMainComponent } from 'src/components/user-main/user-main.component';
import { AccountComponent } from 'src/components/account/account.component';
import { TransactionComponent } from 'src/components/transaction/transaction.component';

@NgModule({
  declarations: [
    AppComponent,
    UserLoginComponent,
    UserMainComponent,
    AccountComponent,
    TransactionComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule.forRoot([
    ]),
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

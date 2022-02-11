import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { combineLatest, Observable, map, startWith } from 'rxjs';
import { DBService } from 'src/services/db/db.service';
import { Account } from 'src/types/Account';
import { User } from '../types/User';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'finance-website';

    user$: Observable<User>;
    accounts$: Observable<Account[]>;

    constructor(private dbService: DBService) {
        this.user$ = combineLatest([
            this.dbService.user$
        ]).pipe(
            map(user => {
                return user[0];
            })
        );

        this.accounts$ = combineLatest([
            this.dbService.accounts$
        ]).pipe(
            map(accounts => {
                return accounts[0];
            })
        );
    }
}

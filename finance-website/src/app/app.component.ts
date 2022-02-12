import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { combineLatest, Observable, map, startWith } from 'rxjs';
import { DBService } from 'src/services/db/db.service';
import { User } from 'src/types/User';
import { Account } from 'src/types/Account';
import { Transaction } from 'src/types/Transaction';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'finance-website';

    user$: Observable<User>;
    accounts$: Observable<Account[]>;
    transactions$: Observable<Transaction[]>;

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

        this.transactions$ = combineLatest([
            this.dbService.transactions$
        ]).pipe(
            map(transactions => {
                return transactions[0];
            })
        );
    }
}

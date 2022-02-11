import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { DBService } from 'src/services/db/db.service';
import { Account } from 'src/types/Account';
import { User } from 'src/types/User';

@Component({
    selector: 'app-user-main',
    templateUrl: './user-main.component.html',
    styleUrls: ['./user-main.component.css']
})
export class UserMainComponent implements OnInit, OnChanges {

    @Input() user: User;
    @Input() accounts: Account[];

    newAccount: Account;

    constructor(private dbService: DBService) { }

    ngOnInit(): void {
        this.newAccount = {
            account_id: "",
            account_balance: 0,
            account_name: "New Account",
            account_type: 0,
            username: this.user.username
        };
    }

    ngOnChanges(changes: SimpleChanges): void {
        
    }

    accountNameChange(val: String) {
        this.newAccount.account_name = val;
    }

    createAccount(acct: Account) {
        this.dbService.newAccount(acct);
    }

    getAccounts(username: String) {
        this.dbService.getAllAccounts(username);
    }
}

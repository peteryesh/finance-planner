import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { DBService } from 'src/services/db/db.service';
import { Account } from 'src/types/Account';
import { Transaction } from 'src/types/Transaction';
import { User } from 'src/types/User';

@Component({
    selector: 'app-user-main',
    templateUrl: './user-main.component.html',
    styleUrls: ['./user-main.component.css']
})
export class UserMainComponent implements OnInit, OnChanges {

    @Input() user: User;
    @Input() accounts: Account[];
    @Input() transactions: Transaction[];

    newAccount: Account;
    newTransaction: Transaction;

    constructor(private dbService: DBService) {}

    ngOnInit(): void {
        this.newAccount = {
            account_id: "",
            account_balance: 0,
            account_name: "New Account",
            account_type: 0,
            username: this.user.username
        };

        this.newTransaction = {
            transaction_id: "",
            name: "",
            date: "",
            amount: 0,
            category: 0,
            notes: "",
            account_id: "",
            username: this.user.username
        }

        this.dbService.getAllAccounts(this.user.username);
    }

    ngOnChanges(changes: SimpleChanges): void {
        
    }

    accountNameChange(val: string) {
        this.newAccount.account_name = val;
    }

    transactionNameChange(val: string) {
        this.newTransaction.name = val;
    }

    // Accounts

    createAccount(acct: Account) {
        this.dbService.newAccount(acct);
    }

    getAccounts(username: string) {
        this.dbService.getAllAccounts(username);
    }

    // Transactions

    createTransaction(transaction: Transaction) {
        this.dbService.newTransaction(transaction);
    }

    getTransactions(username: string) {
        this.dbService.getAllTransactions(username);
    }
}

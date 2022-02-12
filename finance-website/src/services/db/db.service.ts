import { Injectable, OnInit } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, of, switchMap, lastValueFrom } from 'rxjs';
import { map, take } from 'rxjs/operators';
import { User } from '../../types/User';
import { Account } from '../../types/Account';
import { Transaction } from '../../types/Transaction';
import { DBResponse } from 'src/types/DBResponse';

const httpOptions = {
    headers: new HttpHeaders({
        'Content-Type': 'application/json'
    })
}

@Injectable({
    providedIn: 'root'
})
export class DBService implements OnInit {

    dbUrlTest = 'http://localhost:5000';

    private _user: BehaviorSubject<User>;
    user$: Observable<User>;
    private _accounts: BehaviorSubject<Account[]>;
    accounts$: Observable<Account[]>;
    private _transactions: BehaviorSubject<Transaction[]>;
    transactions$: Observable<Transaction[]>;

    constructor(private http: HttpClient) {
        this._user = new BehaviorSubject<User>({username: '', first_name: '', last_name: ''});
        this.user$ = this._user.asObservable();
        this._accounts = new BehaviorSubject<Account[]>([]);
        this.accounts$ = this._accounts.asObservable();
        this._transactions = new BehaviorSubject<Transaction[]>([]);
        console.log(this._transactions.getValue());
        this.transactions$ = this._transactions.asObservable();
    }

    set user(val: User) {
        this._user.next(val);
    }

    ngOnInit() {}

    // User Endpoints

    addOrUpdateUser(user: User) {
        const response = this.http.post(`${this.dbUrlTest}/user`, JSON.stringify(user), httpOptions);
        response.subscribe(event => {console.log(event)});
    }

    async getUser(username: string): Promise<boolean> {
        try {
            const response = await lastValueFrom(this.http.get(`${this.dbUrlTest}/user?username=${username}`)) as DBResponse;
            if (response.success) {
                const user = response.data as User;
                this._user.next(user);
            }
            console.log(response);
            return response.success;
        }
        catch (error) {
            console.error(error);
        }
        return false;
    }

    deleteUser(username: string) {
        const response = this.http.delete(`${this.dbUrlTest}/user?username=${username}`);
        response.subscribe(event => console.log(event));
        return response;
    }

    // Account Endpoints

    async getAccount(acctID: string, username: string) {
        const res = await lastValueFrom(this.http.get(`${this.dbUrlTest}/account?account_id=${acctID}&username=${username}`)) as DBResponse;
        console.log(res);
    }

    async getAllAccounts(username: string) {
        try {
            const res = await lastValueFrom(this.http.get(`${this.dbUrlTest}/account?username=${username}`)) as DBResponse;
            if (res.success) {
                const newAcctArr = res.data as Account[];
                this._accounts.next(newAcctArr);
            }
            console.log(res);
        }
        catch (error) {
            console.error(error);
        }
        return false;
    }

    async newAccount(acct: Account) {
        try {
            const res = await lastValueFrom(this.http.post(`${this.dbUrlTest}/account`, JSON.stringify(acct), httpOptions)) as DBResponse;
            if (res.success) {
                const newAcct = res.data as Account;
                const newAcctArr = this._accounts.getValue();
                newAcctArr.push(newAcct);
                this._accounts.next(newAcctArr);
            }
            console.log(res);
            return res.success;
        }
        catch (error) {
            console.error(error);
        }
        return false;
    }

    updateAccount() {

    }

    deleteAccount() {

    }

    // Transaction Endpoints

    async getAllTransactions(username: string) {
        try {
            const res = await lastValueFrom(this.http.get(`${this.dbUrlTest}/transaction?username=${username}`)) as DBResponse;
            if (res.success) {
                const newTransactionArr = res.data as Transaction[];
                this._transactions.next(newTransactionArr);
            }
            console.log(res);
        }
        catch (error) {
            console.error(error);
        }
        return false;
    }

    async newTransaction(transaction: Transaction) {
        try {
            const res = await lastValueFrom(this.http.post(`${this.dbUrlTest}/transaction`, JSON.stringify(transaction), httpOptions)) as DBResponse;
            if (res.success) {
                const newTransaction = res.data as Transaction;
                const newTransactionArr = this._transactions.getValue();
                console.log(this._transactions.getValue());
                newTransactionArr.push(newTransaction);
                this._transactions.next(newTransactionArr);
            }
            return res.success;
        } catch (error) {
            console.error(error);
        }
        return false;
    }
}

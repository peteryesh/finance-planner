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

    constructor(private http: HttpClient) {
        this._user = new BehaviorSubject<User>({
            username: '',
            first_name: '',
            last_name: ''
        });
        this.user$ = this._user.asObservable();
    }

    set user(val: User) {
        this._user.next(val);
    }

    ngOnInit() {}

    addOrUpdateUser(user: User) {
        const response = this.http.post(`${this.dbUrlTest}/user`, JSON.stringify(user), httpOptions);
        response.subscribe(event => {console.log(event)});
    }

    async viewUser(username: String): Promise<boolean> {
        try {
            const response = await lastValueFrom(this.http.get(`${this.dbUrlTest}/user?username=${username}`)) as DBResponse;
            if (response.success) {
                const user = response.data as User;
                this._user.next(user);
            }
            console.log(response);
            return response.success;
        } catch (error) {
            console.error(error);
        }
        return false;
    }

    deleteUser(username: String) {
        const response = this.http.delete(`${this.dbUrlTest}/user?username=${username}`);
        response.subscribe(event => console.log(event));
        return response;
    }
}

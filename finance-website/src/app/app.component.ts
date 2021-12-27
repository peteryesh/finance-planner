import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';

export interface User {
    username: string;
    first_name: string;
    last_name: string;
}

const httpOptions = {
    headers: new HttpHeaders({
        'Content-Type': 'application/json'
    })
}

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'finance-website';

    testUrl = 'http://localhost:5000';

    user: User = {
        username: '',
        first_name: '',
        last_name: ''
    }


    constructor(private http: HttpClient) { }

    submitUser() {
        const response = this.http.post(`${this.testUrl}/user`, JSON.stringify(this.user), httpOptions);
        response.subscribe(event => console.log(event));
    }

    viewUser() {
        const username = 'petercnoh';
        const response = this.http.get(`${this.testUrl}/user?username=${this.user.username}`);
        response.subscribe(event => console.log(event));
    }

    viewFalseUser() {
        const username = 'somebodyelse';
        const response = this.http.get(`${this.testUrl}/user?username=${this.user.username}`);
        response.subscribe(event => console.log(event));
    }

    deleteUser() {
        const username = 'petercnoh';
        const response = this.http.delete(`${this.testUrl}/user?username=${this.user.username}`);
        response.subscribe(event => console.log(event));
    }

    usernameChange(val: string) {
        this.user.username = val;
    }

    firstNameChange(val: string) {
        this.user.first_name = val;
    }

    lastNameChange(val: string) {
        this.user.last_name = val;
    }
}

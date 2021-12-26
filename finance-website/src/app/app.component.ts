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

    constructor(private http: HttpClient) { }

    submitUser() {
        const new_user = {
            username: 'petercnoh',
            first_name: 'peter',
            last_name: 'noh'
        };
        const response = this.http.post(`${this.testUrl}/adduser`, new_user);
        response.subscribe(event => console.log(event));
    }
}

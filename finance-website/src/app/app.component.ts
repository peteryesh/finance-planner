import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Observable } from 'rxjs';
import { DBService } from 'src/services/db/db.service';
import { User } from '../types/User';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'finance-website';

    user$: Observable<User>;

    constructor(private dbService: DBService) {
        this.user$ = dbService.user$;
    }

    
}

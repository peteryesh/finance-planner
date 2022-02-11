import { Component } from '@angular/core';
import { User } from '../../types/User';
import { DBService } from '../../services/db/db.service';
import { DBResponse } from 'src/types/DBResponse';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-login',
  templateUrl: './user-login.component.html',
  styleUrls: ['./user-login.component.css']
})
export class UserLoginComponent {

    tempUser: User = {
        username: '',
        first_name: '',
        last_name: ''
    }

    constructor(
        private dbService: DBService,
        private router: Router
    ) { }

    usernameChange(val: string) {
        this.tempUser.username = val;
    }

    firstNameChange(val: string) {
        this.tempUser.first_name = val;
    }

    lastNameChange(val: string) {
        this.tempUser.last_name = val;
    }

    async getUserInfo() {
        const res = await this.dbService.getUser(this.tempUser.username);
        if (res) {
            this.router.navigateByUrl(`/`);
        }
        else {
            alert("Error retrieving user");
        }
    }

    addUser() {
        const res = this.dbService.addOrUpdateUser(this.tempUser);
    }
}

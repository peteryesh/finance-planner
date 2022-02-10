import { Component } from '@angular/core';
import { User } from '../../types/User';
import { DBService } from '../../services/db/db.service';
import { DBResponse } from 'src/types/DBResponse';

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

    constructor(private dbService: DBService) { }

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
        const res = await this.dbService.viewUser(this.tempUser.username);
    }

    addUser() {
        const res = this.dbService.addOrUpdateUser(this.tempUser);
    }
}
